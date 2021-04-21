from flask import Flask
from config import Config
from redis import Redis


# Local imports
from app.twofactor import TwoFactorAuth

app = Flask(__name__)
app.config.from_object(Config)

app.redis = Redis.from_url(app.config['REDIS_URI'], charset="utf-8", decode_responses=True)

# Plivo two factor authentication configuration
app.p2fa = TwoFactorAuth(credentials={'auth_id': app.config['PLIVO_AUTH_ID'], 'auth_token': app.config['PLIVO_AUTH_TOKEN']}, app_number=app.config['PLIVO_NUMBER'], phlo_id=app.config['PHLO_ID'])


from app import routes
