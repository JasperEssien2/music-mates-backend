import graphene
from django.db.models import Q
from graphene_django import DjangoObjectType

from .models import Artist, User


class ArtistType(DjangoObjectType):
    class Meta:
        model = Artist
        fields = ("id", "name", "image_url", "description")


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "name", "google_id",
                  "image_url", "favourite_artists")


class Query(graphene.ObjectType):

    all_artists = graphene.List(ArtistType)

    def resolve_all_artists(root, info):
        return Artist.objects.all()

    user_favourite_artist = graphene.List(
        ArtistType, args={'user_id': graphene.Int()})

    def resolve_user_favourite_artist(root, info, user_id):

        return Artist.objects.filter(favourite_users__id=user_id)

    user_info = graphene.Field(UserType, google_id=graphene.String())

    def resolve_user_info(root, info, google_id):
        return User.objects.get(google_id=google_id)

    music_mates = graphene.List(UserType, args={'user_id': graphene.Int()})

    def resolve_music_mates(root, info, user_id):
        favourite_artist = Artist.objects.filter(
            favourite_users__id=user_id)

        return User.objects.filter(favourite_artists__in=favourite_artist).filter(~Q(pk=user_id))


class UserMutation(graphene.Mutation):

    class Arguments:
        name = graphene.String(required=True)
        google_id = graphene.String(required=True)
        image_url = graphene.String(required=True)
        favourite_artists = graphene.List(graphene.ID)

    user = graphene.Field(UserType)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        artists = Artist.objects.filter(pk__in=kwargs['favourite_artists'])

        user = User(
            name=kwargs['name'], google_id=kwargs['google_id'], image_url=kwargs['image_url'])
        user.save()

        user.favourite_artists.set(artists)

        return UserMutation(user=user)


class Mutation(graphene.ObjectType):

    create_user = UserMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
