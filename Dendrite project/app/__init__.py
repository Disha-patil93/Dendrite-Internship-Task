# app/__init__.py
from flask import Flask
from flask_graphql import GraphQLView
from flask_security import Security, SQLAlchemyUserDatastore
from flask_graphql_auth import GraphQLAuth
from flask_stripe import Stripe
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.py')
CORS(app)


db = SQLAlchemy(app)
migrate = Migrate(app, db)

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

auth = GraphQLAuth(app)


stripe = Stripe(app)


from .models import User, Role, Todo
from .queries import Query
from .mutations import Mutation
from .routes import *


app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))
