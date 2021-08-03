import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from xml.sax.saxutils import unescape
from datetime import datetime


# WordPress接続情報
WP_URL = '自分のサイトのURL'
WP_USERNAME = '管理画面ログイン時のユーザネーム'
WP_PASSWORD = 'xxxx xxxx xxxx xxxx' #ユーザ設定で発行したパスワード(管理画面のパスワードとは別)



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



# 記事を下書き投稿する
res = post_article('draft',
                   'test-path',
                   title,
                   html_text,
                   category_ids=[2],
                   tag_ids=[5,6],
                   media_id=759)


