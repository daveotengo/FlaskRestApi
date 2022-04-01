from flask import Flask,request,abort
from flask_restful import Api, Resource,reqparse

app = Flask(__name__)
api = Api(app)

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video required",required=True)
video_put_args.add_argument("views", type=str, help="Views of the video required",required=True)
video_put_args.add_argument("likes", type=str, help="Likes of the video required",required=True)


videos = {}

def abort_if_video_id_doesnt_exist(video_id):
    if video_id not in videos:
        abort(404, "Could not find video...")

def abort_if_video_id_exist(video_id):
    if video_id in videos:
        abort(409, "Video with id: {0} already exists".format(video_id))

class Video(Resource):
    
    def get(self,video_id):
        abort_if_video_id_doesnt_exist(video_id)
        return videos[video_id]

    def put(self,video_id):
        abort_if_video_id_exist(video_id)
        args = video_put_args.parse_args()
        print(args)
        videos[video_id] = args
        #print(request.form["likes"])
        return videos[video_id], 201

    def delete(self,video_id):
        abort_if_video_id_doesnt_exist(video_id)
        del videos[video_id]
        return '',204

    def post(self):
        return {"data":"Posted"}

api.add_resource(Video, "/video/<int:video_id>")

if __name__=="__main__":
    app.run(debug=True)