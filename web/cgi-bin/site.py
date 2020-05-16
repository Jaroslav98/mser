#!/usr/bin/env python3
# python3 -m http.server --cgi
# http://localhost:8000/cgi-bin/site.py

from client1 import get_articles


id_list, title_list, author_list, href_list = get_articles()
new_line = "<br>"
like = """<input name="dis_like{i}" type="radio" class="radio"
       value="like{article_id}" id="t"/><label for="t">like</label>"""
dislike = """<input name="dis_like{i}" type="radio" class="radio"
          value="dislike{article_id}" id="f"/><label for="f">dislike</label>"""
submit = """<input type="submit"></input>"""


print("Content-type: text/html")
print("<link rel='stylesheet' type='text/css' href='try.css'>")
print()
print('<form action="form.py" method="get">')

for i in range(len(id_list)):
    print(f"<a href='{href_list[i]}'>{title_list[i]}</a> {new_line}")
    print(f'<fieldset><div class="some-class">'
          f'{like.format(i=i, article_id=title_list[i])}  {dislike.format(i=i, article_id=title_list[i])}</div></fieldset>')

print(f'{submit.format(i=i)}</form>')
