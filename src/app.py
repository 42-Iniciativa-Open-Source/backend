from flask import Flask
import logging
import json

from routes import forty_two

app = Flask(__name__)

app.register_blueprint(forty_two.bp)

logging.basicConfig(filename="logs/middleman.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)

@app.route('/')
def middleman():
    return {"Success": "You can successfully communicate with the middleman backend."}, 200

if __name__ == '__main__':
    app.run("127.0.0.1", 4242)
