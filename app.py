import datetime
import json
import uuid
import os

from flask import Flask, json, Response
from utils.logutil import Logger
from extractors.ingredient import IngredientExtractor

app = Flask(__name__)
app.config.from_pyfile('config.py')

# Only call this once in the entire application
Logger().setupLogger()


@app.route('/')
def site_default():
    return """
    <html>
    <head>
        <title>Recipe Extract API Service</title>
        <style type="text/css">
            html, body { font-family: sans-serif; font-size: 12px; }
        </style>
    </head>
    <body>
    <h2>Recipe Extract API Service</h2>
    </body>
    </html>
    """


@app.route('/extract')
def extract():
    file_path = os.path.join(os.path.dirname(__file__), "./samples/butternut_squash_soup.txt")
    with open(file_path) as reader:
        content = reader.read()
    extractor = IngredientExtractor()
    return get_json_response(extractor.extract_text(content))


def json_default(value):
    if isinstance(value, datetime.date):
        return value.isoformat()
    else:
        return value.__dict__


def get_json_response(result):
    return Response(json.dumps(result, default=json_default,
                               sort_keys=True, indent=4), mimetype='application/json')


if __name__ == '__main__':
    Logger().getLogger().info('Recipe Extractor Service Started')
    app.run(host='0.0.0.0')
    app.config.update(
        SECRET_KEY = str(uuid.uuid4()),
        PROPAGATE_EXCEPTIONS = True,
        PRESERVE_CONTEXT_ON_EXCEPTION = True
    )