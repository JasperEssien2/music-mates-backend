
import graphene
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
        ArtistType, args={'favourite_artist_ids': graphene.List(graphene.Int)})

    def resolve_user_favourite_artist(root, info, favourite_artist_ids):
        return Artist.objects.filter(pk__in=favourite_artist_ids)

    user_info = graphene.Field(UserType, google_id=graphene.String())

    def resolve_user_info(root, info, google_id):
        return User.objects.get(google_id=google_id)


class Mutation(graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
