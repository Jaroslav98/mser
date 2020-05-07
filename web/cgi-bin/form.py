#!/usr/bin/env python3
import cgi
from pymongo import MongoClient
from client1 import get_articles

SERVER_HOST = 'mongodb://localhost:27017/'
SERVER_DB = 'verge'
SERVER_COLLECTION = 'articles_stats'

LIKE = 'like'
DISLIKE = 'dislike'

id_list, title_list, author_list, href_list = get_articles()

form = cgi.FieldStorage()

print("Content-type: text/html")
print()


def store_in_db(article_id, ld_value):
    client = MongoClient(SERVER_HOST)
    db = client[SERVER_DB]
    col = db[SERVER_COLLECTION]
    col.insert_one({
        "article_id": article_id,
        "like_dislike": ld_value,
        "app_type": "web"
    })


likes, dislikes = 0, 0
for i in range(len(id_list)):
    try:
        like_dislike_name = f'dis_like{i}'
        like_dislike_value = form.getvalue(like_dislike_name)
        if DISLIKE in like_dislike_value:
            dislikes += 1
            store_in_db(like_dislike_value[7:], DISLIKE)
        elif LIKE in like_dislike_value:
            likes += 1
            store_in_db(like_dislike_value[4:], LIKE)
    except:
        continue
print(f'Total stored: likes = {likes}, dislikes = {dislikes}')
