
from graphene import ObjectType, List, Field, String
from flask_graphql_auth import query_jwt_required
from flask_security import current_user
from .models import Todo

class TodoType(ObjectType):
    id = String()
    title = String()
    description = String()
    time = String()

class Query(ObjectType):
    todos = List(TodoType)

    @query_jwt_required
    def resolve_todos(self, info):
        user_id = current_user.id
        todos = Todo.query.filter_by(user_id=user_id).all()
        return todos
