from flask import Flask

app = Flask(__name__)


@app.route("/alma", methods=['POST'])
def render():
    return {"movies": "aha"}


if __name__ == '__main__':
    app.run()
