
from graphene import ObjectType, String, Mutation, Field
from flask_graphql_auth import mutation_jwt_required
from flask_security import current_user
from .models import Todo, db

class AddTodoMutation(Mutation):
    class Arguments:
        title = String(required=True)
        description = String()
        time = String()

    todo = Field(lambda: TodoType)

    @mutation_jwt_required
    def mutate(self, info, title, description=None, time=None):
        user_id = current_user.id
        new_todo = Todo(title=title, description=description, time=time, user_id=user_id)
        db.session.add(new_todo)
        db.session.commit()
        return AddTodoMutation(todo=new_todo)

class DeleteTodoMutation(Mutation):
    class Arguments:
        todo_id = String(required=True)

    message = String()

    @mutation_jwt_required
    def mutate(self, info, todo_id):
        user_id = current_user.id
        todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()

        if not todo:
            return DeleteTodoMutation(message='Todo not found or unauthorized')

        db.session.delete(todo)
        db.session.commit()

        return DeleteTodoMutation(message='Todo deleted successfully')

class EditTodoMutation(Mutation):
    class Arguments:
        todo_id = String(required=True)
        title = String()
        description = String()
        time = String()

    message = String()

    @mutation_jwt_required
    def mutate(self, info, todo_id, title=None, description=None, time=None):
        user_id = current_user.id
        todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()

        if not todo:
            return EditTodoMutation(message='Todo not found or unauthorized')

        todo.title = title or todo.title
        todo.description = description or todo.description
        todo.time = time or todo.time

        db.session.commit()

        return EditTodoMutation(message='Todo edited successfully')

class Mutation(ObjectType):
    add_todo = AddTodoMutation.Field()
    delete_todo = DeleteTodoMutation.Field()
    edit_todo = EditTodoMutation.Field()
