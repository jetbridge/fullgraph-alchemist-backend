import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
from fga.model import Item
from fga.gql.user.schema import UserSchema


class ItemSchema(SQLAlchemyObjectType):
    id_ = graphene.Int(description="id_ of item")
    key = graphene.String(description="item key")
    value = graphene.JSONString(description="dictionary on the item object")
    user = graphene.Field(UserSchema, description="user who owns the item")

    class Meta:
        model = Item
        interfaces = (relay.Node,)
