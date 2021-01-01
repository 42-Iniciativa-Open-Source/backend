from flask import Flask, request
import logging

from routes import forty_two
from constants import AUTHORIZATION_CODE

app = Flask(__name__)

app.register_blueprint(forty_two.bp)

logging.basicConfig(
    filename="logs/middleman.log",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)


@app.route('/')
def index():
    header_authorization_code = request.headers.get("Authorization")
    if AUTHORIZATION_CODE == header_authorization_code:
        return {}, 200
    return {}, 401
