

import os

class Config:
    SECRET_KEY = 'disha'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True  
    STRIPE_PUBLIC_KEY = 'disha@123'
    STRIPE_SECRET_KEY = '123456'
    GRAPHQL_PLAYGROUND_ENABLED = True 

    
    SQLALCHEMY_DATABASE_URI = os.environ.get('sqlite:///site.db') 

    
    SECURITY_PASSWORD_SALT = '123'
    SECURITY_PASSWORD_HASH = 'bcrypt' 

    
    JWT_SECRET_KEY = '12345'

    
    KEYCLOAK_REALM = 'Dendrite project'
    KEYCLOAK_CLIENT_ID = '456'
    KEYCLOAK_CLIENT_SECRET = 'dishaapp'
    KEYCLOAK_BASE_URL = 'https://auth/DENDRITE'

    
    STRIPE_API_KEY = 'Disha'
    STRIPE_SUCCESS_URL = 'http://localhost:5000/success'
    STRIPE_CANCEL_URL = 'http://localhost:5000/cancel'


if os.environ.get('FLASK_ENV') == 'production':
    class ProductionConfig(Config):
        DEBUG = False
        GRAPHQL_PLAYGROUND_ENABLED = False

    config = ProductionConfig()
else:
    config = Config()
