import graphene
from graphene import relay
from graphene.types.json import JSONString
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db_session, Department as DepartmentModel, Video as VideoModel


class Department(SQLAlchemyObjectType):
    class Meta:
        model = DepartmentModel
        interfaces = (relay.Node, )


class Video(SQLAlchemyObjectType):
    class Meta:
        model = VideoModel
        interfaces = (relay.Node, )


class CreateVideo(graphene.Mutation):

    class Arguments:
        name = graphene.String()
        likes = graphene.Int()
        views = graphene.Int()
        #department_id = graphene.Int()

    ok = graphene.Boolean()
    video = graphene.Field(Video)

    @classmethod
    def mutate(cls, _, info, **args):
        video = VideoModel(name=args.get('name'),
                                 likes=args.get('likes'),
                                 views=args.get('views'))
                                 #department_id=args.get('department_id'))
        db_session.add(video)
        db_session.commit()
        ok = True
        return CreateVideo(video=video, ok=ok)


class UpdateVideo(graphene.Mutation):

    class Arguments:
        name = graphene.String()
        likes = graphene.Int()
        views = graphene.Int()
        #department_id = graphene.Int()

    ok = graphene.Boolean()
    video = graphene.Field(Video)

    @classmethod
    def mutate(cls, _, info, **args):
        query = Video.get_query(info)
        print("print query")
        print(query)

        video = query.filter(VideoModel.name == args.get('name')).first()
        print("print video")
        print(video)
        video.name = args.get('name')
        video.likes = args.get('likes')
        video.views = args.get('views')
        db_session.commit()
        ok = True
       

        return UpdateVideo(video=video, ok=ok)


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    videos = SQLAlchemyConnectionField(Video)
    print("printing videos")
    print(videos)
    departments = SQLAlchemyConnectionField(Department)
    video = graphene.Field(Video, name=graphene.String())
    department = graphene.Field(Department, name=graphene.String())


    def resolve_video(self, info, name):
        query = Video.get_query(info)
        print(info)
        print("printing query")
        print(query)
        return query.filter(VideoModel.name == name).first()
    
    def resolve_department(self, info, name):
        query = Department.get_query(info)
        print(info)
        print("printing query")
        print(query)
        return query.filter(DepartmentModel.name == name).first()


class MyMutations(graphene.ObjectType):
    create_video = CreateVideo.Field()
    update_video = UpdateVideo.Field()


schema = graphene.Schema(query=Query, mutation=MyMutations, types=[Department, Video])
