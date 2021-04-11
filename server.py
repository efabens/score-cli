from flask import Flask
from flask_restful import Api, Resource
from nba_cli import run
from utility import ansi_to_html


from flask import Flask, url_for
app = Flask(__name__)


@app.route('/')
def api_root():
    return ansi_to_html(run())


if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=8080)
