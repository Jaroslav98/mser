# 127.0.0.1:5000
import graphene
import mongoengine
from flask import Flask
from flask_graphql import GraphQLView
from graphene.relay import Node
from graphene_mongo import MongoengineObjectType, MongoengineConnectionField
from mongoengine import Document
from mongoengine.fields import StringField

# Configs
app = Flask(__name__)
app.debug = True
app.config['MONGODB_SETTINGS'] = {'db': 'verge', 'alias': 'default'}
app.config['MONGOALCHEMY_DATABASE'] = 'verge'
mongoengine.connect('verge', alias='default')


# Models
class articles(Document):
    meta = {'db_alias': 'default', 'collection': 'articles'}
    _id = StringField(required=True)
    id = StringField(required=True)
    title = StringField(required=True)
    author = StringField(required=True)
    href = StringField(required=True)
    date = StringField(required=True)


# Schema Objects
class ArticleObject(MongoengineObjectType):
    class Meta:
        model = articles
        interfaces = (Node,)


class Query(graphene.ObjectType):
    node = Node.Field()
    all_articles = MongoengineConnectionField(ArticleObject)


schema = graphene.Schema(query=Query, types=[ArticleObject])
# Routes
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True
    )
)


if __name__ == '__main__':
     app.run()
