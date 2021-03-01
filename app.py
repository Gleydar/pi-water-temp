import threading

from flask import Flask, render_template
import json

from SensorReader import SensorReader

app = Flask(__name__)


def load_json():
    with open('static/data.json') as f:
        return json.load(f)


@app.route('/')
def hello_world():
    return render_template('main.html.jinja', data=load_json())


if __name__ == '__main__':
    reader = SensorReader()
    threading.Thread(target=reader.loop)
    app.run()

