import graphene
from graphene_django.types import DjangoObjectType
from graphql import GraphQLError

from django.contrib.auth import get_user_model


'''
App models

'''


User = get_user_model()


from survey.models import (

        Survey,
        Question,
        Response

    )


from userprofile.models import(

    UserProfile

    )



        # The User Model


class UserType(DjangoObjectType):

    class Meta:
        model = User


        # The Profile Model

class ProfileType(DjangoObjectType):

    class Meta:

        model = UserProfile

    # avatar          = graphene.String()
    # cover_photo     = graphene.String()


    # def resolve_avatar(self, info):

    #     return info.context.build_absolute_uri(self.avatar.url)

    # def resolve_cover_photo(self, info):

    #     return info.context.build_absolute_uri(self.cover_photo.url)


        # The Survey Model


class SurveyType(DjangoObjectType):

    class Meta:

        model = Survey

    # featured_image = graphene.String()

    # gallery_images = graphene.String()

    # def resolve_featured_image(self, info):

    #     return info.context.build_absolute_uri(self.featured_image.url)

    # def gallery_images(self, info):

    #     return info.context.build_absolute_uri(self.gallery_images)



        # The Survey Model


class QuestionType(DjangoObjectType):

    class Meta:

        model = Question

        # The Response Model


class ResponseType(DjangoObjectType):

    class Meta:
        model = Response

       




class Query(graphene.ObjectType):

    # The User Detail

    me              =   graphene.Field(UserType)

    # The Profile Detail

    profile         =   graphene.Field(ProfileType)

    # The Survey List and Detail Query

    Surveys           =   graphene.List(SurveyType)
    Survey            =   graphene.Field(SurveyType, id = graphene.Int())

    # The Question List and Detail Query

    questions         =   graphene.List(QuestionType)
    question          =   graphene.Field(QuestionType, id = graphene.Int())

    # The Response List and Detail Query


    responses        =   graphene.List(ResponseType)
    response         =   graphene.Field(ResponseType, id = graphene.Int())





    # The User Detail Resolve Method


    def resolve_me(self, info, **kwargs):

        user    =  info.context.user
        if user.is_anonymous:
            raise GraphQLError("You Must be authenticated to access this User")

        else:

            return user

    # The Profile Detail Resolve method

    def resolve_profile(self, info, **kwargs):

        user     = info.context.user

        if user.is_anonymous:

            raise GraphQLError('You must be authenticated to view this profile')

        else:

            return user.profile

    # The Survey List and Detail Resolve  Method

    def resolve_surveys(self, info, **kwargs):

        user        =  info.context.user

        if user.is_anonymous:

            raise GraphQLError("You must be authenticated to view this guides")

        else:

            return Tour.objects.all()


    def resolve_survey(self, info, **kwargs):

        user        = info.context.user
        id          = kwargs.get('id')

        if user.is_anonymous:

            raise GraphQLError("you must be authenticated to view this guide")

        else:
            return Tour.objects.get(pk = id)


    # The Question List and Detail Resolve Method


    def resolve_questions(self, info, **kwargs):

        user        =  info.context.user

        if user.is_anonymous:

            raise GraphQLError("You must be authenticated to view this posts")

        else:
            return Post.objects.filter(user= user)

    def resolve_question(self, info, **kwargs):

        user        = info.context.user
        id          = kwargs.get('id')
        if user.is_anonymous:
            raise GraphQLError("You must be authenticated to view this post")

        else:
            return Post.objects.get(pk = id)

    # The response List and Detail Resolve Method


    def resolve_responses(self, info, **kwargs):

        user        =   info.context.user
        pass


    def resolve_response(self, info, **kwargs):

        pass











