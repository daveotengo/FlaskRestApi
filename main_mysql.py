from flask import Flask,request,abort
from flask_restful import Api, Resource,reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from schema import schema
from flask_graphql import GraphQLView

app = Flask(__name__)
api = Api(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Dadapapa4141@localhost:3306/alch_db?charset=utf8mb4'

db = SQLAlchemy(app)
print(db)


class VideoModel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name={self.name},views={self.views},likes={self.likes})"

# db.create_all()
# db.session.commit()


video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video required",required=True)
video_put_args.add_argument("views", type=str, help="Views of the video required",required=True)
video_put_args.add_argument("likes", type=str, help="Likes of the video required",required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video required")
video_update_args.add_argument("views", type=str, help="Views of the video required")
video_update_args.add_argument("likes", type=str, help="Likes of the video required")


videos = {}

def abort_if_video_id_doesnt_exist(video_id):
    if video_id not in videos:
        abort(404, "Could not find video...")

def abort_if_video_id_exist(video_id):
    if video_id in videos:
        abort(409, "Video with id: {0} already exists".format(video_id))

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}

class Video(Resource):
    @marshal_with(resource_fields)
    def get(self,video_id):
        #abort_if_video_id_doesnt_exist(video_id)
        result=VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, "Could not find video...")
        return result

  
        
    # @marshal_with(resource_fields)
    # def put(self,video_id):
    #     #abort_if_video_id_exist(video_id)
    #     result=VideoModel.query.filter_by(id=video_id).first()
    #     if result:
    #         abort(409, "Video with id: {0} already exists".format(video_id))

    #     args = video_put_args.parse_args()
    #     print(args)
    #     video = VideoModel(id=video_id,name=args['name'],views=args['views'],likes=args['likes'])
    #     db.session.add(video)
    #     db.session.commit()
    #     #print(request.form["likes"])
    #     return video, 201

    @marshal_with(resource_fields)
    def put(self,video_id):
        #abort_if_video_id_exist(video_id)
        result=VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, "Video with id: {0} does not exists".format(video_id))
 
        args = video_update_args.parse_args()
        print(args)

        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']
         
        #db.session.add(result)
        db.session.commit()
        #print(request.form["likes"])
        return result

    

    def delete(self,video_id):
        #abort_if_video_id_doesnt_exist(video_id)
        result=VideoModel.query.filter_by(id=video_id).first()

        if not result:
            abort(404, "Could not find video...")
        try:
            db.session.delete(result)
            db.session.commit()
        except:
            return "There was a problem deleting record."
        return '',204

    def post(self):
        return {"data":"Posted"}

class VideoPostNGetAll(Resource):
    @marshal_with(resource_fields)
    def post(self):
        args = video_put_args.parse_args()
        print(args)
        #abort_if_video_id_exist(video_id)
        name = args['name']
        result=VideoModel.query.filter_by(name=name).first()
        if result:
            abort(409, "Video with name: {0} already exists".format(name))
      
        video = VideoModel(name=args['name'],views=args['views'],likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        #print(request.form["likes"])
        return video, 201
    
    @marshal_with(resource_fields)
    def get(self):
        #abort_if_video_id_doesnt_exist(video_id)
        result=VideoModel.query.all()
        if not result:
            result =[]
        return result

api.add_resource(Video, "/video/<int:video_id>")
api.add_resource(VideoPostNGetAll, "/video")


app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))


if __name__=="__main__":
    app.run(debug=True,host='localhost',port=5004)