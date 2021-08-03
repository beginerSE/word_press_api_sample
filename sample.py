import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from xml.sax.saxutils import unescape
from datetime import datetime


# WordPress接続情報
WP_URL = 'https://tkdmjtmj.xsrv.jp'
WP_USERNAME = 'oruka'
WP_PASSWORD = 'MFlP KCTz r06F 9FMi fUpV eaQ2'


def generate_html(url):
    # リクエストヘッダー
    headers = {
        'User-Agent':'Mozilla/5.0'
    }

    #URLリソースを開く
    res = requests.get(url, headers=headers)
    unker_data = []
    main_data = []
    unker_number = []

    #インスタンスの作成
    soup = BeautifulSoup(res.text, "html.parser")
    title = soup.find_all('h1', class_='title')[0].text
    posts = soup.find_all('div', class_='post')
    for post in posts:
#         print(post)
        name = post.find_all('span', class_='name')[0].text
#         if '名無し' in name:
        try:
            number = post.find_all('span', class_='number')[0].text
            date = post.find_all('span', class_='date')[0].text
            uid = post.find_all('span', class_='uid')[0].text
            text = post.find_all('span', class_='escaped')[0]
            try:
                for tag in text.find_all('a', class_='image'):
                    tag.replace_with('<img src="' + tag.text + '" width="400" height="400"></img>')
            except:
                pass
            if '>>' in post.text:
                p = r'>>(.+?) '
                unker_address = re.findall(p, post.text)[0]
                unker_data.append([number, date, uid, unker_address,text])
            else:
                unker_address = ''
                main_data.append([number, date, uid, unker_address, text])
        except:
            pass

    main_df = pd.DataFrame(main_data)
    unker_df = pd.DataFrame(unker_data)

    html_text = ''
    post_count = 0 
    for i in range(len(main_df)):
        unker_count = 0
        post_count += 1
        if post_count <= 30:
            if post_count%10 == 0 :
                html_text +='<br /><script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script><!-- 自動サイズ -->' + \
                '<ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-5249770121737505"data-ad-slot="2988664274"data-ad-format="auto"></ins>' + \
                '<script>(adsbygoogle = window.adsbygoogle || []).push({});</script><br />'
            ex_data = unker_df[unker_df[3] == str(main_df.iloc[i][0])]
            if len(ex_data) > 1:
                html_text += '<p><strong>' + str(main_df.iloc[i][0])+ \
                ' </strong><span style="color: #00ff00;opacity: 0.5;">名無しさん</span><span style="opacity: 0.5;"> '+ \
                str(main_df.iloc[i][1]) + ' ' +str(main_df.iloc[i][2])+'</span></p><strong><div style="font-size:22px;color:#ff4500;">'+ \
                str(main_df.iloc[i][3])+'<br />' +str(main_df.iloc[i][4])+'</div></strong><br /><br /><hr style="opacity: 0.5;">'
            else:
                html_text += '<p><strong>' + str(main_df.iloc[i][0])+ \
                ' </strong><span style="color: #00ff00;opacity: 0.5;">名無しさん</span><span style="opacity: 0.5;"> '+ \
                str(main_df.iloc[i][1]) + ' ' +str(main_df.iloc[i][2])+'</span></p><strong><div style="font-size:22px;">'+ \
                str(main_df.iloc[i][3])+'<br />' +str(main_df.iloc[i][4])+'</div></strong><br /><br /><hr style="opacity: 0.5;">'
            if len(ex_data) != 0:
                for u in range(len(ex_data)):
                    unker_count += 1
                    if unker_count <= 3:
                        html_text += '<p><strong>' + str(ex_data.iloc[u][0])+ \
                        ' </strong><span style="color: #00ff00;opacity: 0.5;">名無しさん</span><span style="opacity: 0.5;"> '+ \
                        str(ex_data.iloc[u][1]) + ' ' +str(ex_data.iloc[u][2])+'</span></p><strong><span style="font-size:22px;">'+ \
                        '<br />' +str(ex_data.iloc[u][4])+'</span></strong><br /><br /><hr style="opacity: 0.5;">'

    html_text += "<br /><br /><br /><br /><p>参照先" + '  ' + url + '</p><br /><br />'
    html_text = unescape(html_text)
    
    try:
        int(title[-1])
        title = title[:-1]
    except:
        pass
    path = url[-7:]

    return path, title[:40], html_text


# WordPress新規投稿関数
def post_article(status, slug, title, content, category_ids, tag_ids, media_id):
    # REST APIを使うための認証情報
    user_ = WP_USERNAME
    pass_ = WP_PASSWORD
    # 投稿記事情報
    payload = {"status": status,                     #ステータス 公開：publish, 下書き：draft
              "slug": slug,                         #URLスラッグ
              "title": title,                       #タイトル
              "content": content,                   #内容
              "date": datetime.now().isoformat(),   #投稿日時
              "categories": category_ids,           #カテゴリー
              "tags": tag_ids}                      #タグ
    if media_id is not None:
        payload['featured_media'] = media_id         #アイキャッチ画像

    # 記事の新規投稿を行う
    res = requests.post(urllib.parse.urljoin(WP_URL, "wp-json/wp/v2/posts"),     #"wp-json/wp/v2/posts"にPostすると新規投稿になる
                       json=payload,                                            #投稿する記事の内容を設定する
                       auth=(user_, pass_))                                   #ユーザ、パスワードを設定する
    
    return res


path, title, send_text = generate_html('http://egg.5ch.net/test/read.cgi/bizplus/1627644504')

# 記事を下書き投稿する
res = post_article('publish',
                   path,
                   title,
                   send_text,
                   category_ids=[2],
                   tag_ids=[5,6],
                   media_id=None)
