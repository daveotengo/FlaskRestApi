from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self,name,test):
        return {"data":"HelloWorld","name":name,"test":test}

    def post(self):
        return {"data":"Posted"}

api.add_resource(HelloWorld, "/helloWorld/<string:name>/<int:test>")

if __name__=="__main__":
    app.run(debug=True)