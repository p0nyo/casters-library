# init .py
from pathlib import Path

from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object('config.Config')
    data_path = Path('podcast')/'adapters'/'data'
    if test_config is not None:
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH'
        ]