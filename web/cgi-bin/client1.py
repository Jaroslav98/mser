# docker run -p 6379:6379 --rm --name redis redis

import requests
from redis_dec import Cache
from redis import StrictRedis

headers = {"Authorization": "Bearer YOUR API KEY"}


def run_query(query):
    request = requests.post('http://127.0.0.1:5000/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))


# The GraphQL query
query = """
{
  allArticles {
    edges {
      node {
        id
        title
        author
        href
      }
    }
  }
}
"""

# Cache
redis = StrictRedis(decode_responses=True)
cache = Cache(redis)


@cache.list(100)
def get_articles():
    result = run_query(query)

    new_w = {}
    for i in range(2):
        for s in result.values():
            new_w.update(**s)
        result = new_w
        new_w = {}

    data = result["edges"]

    id_list = []
    title_list = []
    author_list = []
    href_list = []

    for i in range(len(data)):
        new_w2 = {}
        for s in data[i].values():
            new_w2.update(**s)
        id_list.append(new_w2["id"])
        title_list.append(new_w2["title"])
        author_list.append(new_w2["author"])
        href_list.append(new_w2["href"])
    return id_list, title_list, author_list, href_list


if __name__ == "__main__":
    get_articles()
    id_list, title_list, author_list, href_list = get_articles()
    print(id_list)
