from flask import Flask
from routes import Config, GetConfig
from flask_restful import Api

app = Flask(__name__)
api = Api(app)


@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"


api.add_resource(GetConfig, '/config/<key>')
api.add_resource(Config, '/config')


if __name__ == "__main__":
    app.run(host='0.0.0.0')
