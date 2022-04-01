from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

names = {
    "tim": {"age": 16,"gender": "male"},
    "bill": {"age": 70,"gender": "female"}
}

class HelloWorld(Resource):
    def get(self,name):
        return names[name]

    def post(self):
        return {"data":"Posted"}

api.add_resource(HelloWorld, "/helloWorld/<string:name>")

if __name__=="__main__":
    app.run(debug=True)