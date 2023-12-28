
from flask import render_template, request, redirect, url_for, jsonify
from flask_security import login_required, current_user
from flask_graphql_auth import get_jwt_identity, mutation_jwt_required
from .models import Todo, db
from .queries import Query
from .mutations import Mutation
from .schema import schema


@login_required
def graphql_playground():
    return render_template('graphql_playground.html')

# GraphQL endpoint
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True),
    methods=['POST', 'GET']
)


@app.route('/add_todo', methods=['POST'])
@mutation_jwt_required
def add_todo():
    user_id = get_jwt_identity()
    data = request.json
    title = data.get('title')
    description = data.get('description')
    time = data.get('time')

    new_todo = Todo(title=title, description=description, time=time, user_id=user_id)
    db.session.add(new_todo)
    db.session.commit()

    return jsonify({'message': 'Todo added successfully!'}), 201


@app.route('/delete_todo/<int:todo_id>', methods=['DELETE'])
@mutation_jwt_required
def delete_todo(todo_id):
    user_id = get_jwt_identity()
    todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()

    if not todo:
        return jsonify({'message': 'Todo not found or unauthorized'}), 404

    db.session.delete(todo)
    db.session.commit()

    return jsonify({'message': 'Todo deleted successfully!'}), 200


@app.route('/edit_todo/<int:todo_id>', methods=['PUT'])
@mutation_jwt_required
def edit_todo(todo_id):
    user_id = get_jwt_identity()
    todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()

    if not todo:
        return jsonify({'message': 'Todo not found or unauthorized'}), 404

    data = request.json
    todo.title = data.get('title', todo.title)
    todo.description = data.get('description', todo.description)
    todo.time = data.get('time', todo.time)

    db.session.commit()

    return jsonify({'message': 'Todo edited successfully!'}), 200
