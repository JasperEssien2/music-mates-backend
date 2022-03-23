import graphene
from django.db.models import Q
from graphene_django import DjangoListField, DjangoObjectType

from .models import Artist, User

# Specifies the schema type [ArtistType] and declares its field
class ArtistType(DjangoObjectType):
    class Meta:
        model = Artist
        fields = ("id", "name", "image_url", "description")

# Specifies the schema type [UserType] and declares its field
class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "name", "google_id",
                  "image_url", "favourite_artists")


class Query(graphene.ObjectType):

     # GraphQL automatically changes this to a camel case name [allArtists]
    all_artists = DjangoListField(ArtistType)

    # GraphQL automatically changes this to a camel case name [userFavouriteArtist]
    # We also specify the args named [google_id], which we used in frontend code
    user_favourite_artist = graphene.List(
        ArtistType, args={'google_id': graphene.String()})

    # This methods resolves the query by returning all artist in the database 
    def resolve_user_favourite_artist(root, info, google_id):

        return Artist.objects.filter(favourite_users__google_id=google_id)
 
    user_info = graphene.Field(UserType, google_id=graphene.String())

    # This methods resolves the userInfo query by quering the database for a user object with the googleId 
    def resolve_user_info(root, info, google_id):
        return User.objects.get(google_id=google_id)

    music_mates = graphene.List(
        UserType, args={'google_id': graphene.String()})

    # This methods resolves the musicMates query by quering the database for users 
    # that shares favourite artists with the user with this googleId 
    def resolve_music_mates(root, info, google_id):
        favourite_artist = Artist.objects.filter(
            favourite_users__google_id=google_id)

        return User.objects.filter(favourite_artists__in=favourite_artist).filter(~Q(google_id = google_id)).distinct()

schema = graphene.Schema(query=Query, mutation=Mutation)

class CreateUserMutation(graphene.Mutation):

    class Arguments:
        name = graphene.String(required=True)
        google_id = graphene.String(required=True)
        image_url = graphene.String(required=True)
        favourite_artists = graphene.List(graphene.ID)
        is_update = graphene.Boolean()

    user = graphene.Field(UserType)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        try:
            exisiting_user = User.objects.get(google_id=kwargs['google_id'])

            return CreateUserMutation(user=exisiting_user)
        except:
            user = User(
                name=kwargs['name'], google_id=kwargs['google_id'], image_url=kwargs['image_url'])

            artists = Artist.objects.filter(pk__in=kwargs['favourite_artists'])
            user.save()

            user.favourite_artists.set(artists)

            return CreateUserMutation(user=user)


class UpdateUserMutation(graphene.Mutation):

    class Arguments:
        name = graphene.String()
        google_id = graphene.String(required=True)
        image_url = graphene.String()
        favourite_artists = graphene.List(graphene.ID)

    user = graphene.Field(UserType)

    @classmethod
    def mutate(cls, root, info, **kwargs):

        exisiting_user = User.objects.get(google_id=kwargs['google_id'])

        artists = Artist.objects.filter(pk__in=kwargs['favourite_artists'])

        exisiting_user.favourite_artists.set(artists)
        
        try:
            if(kwargs['name'] != None):
                exisiting_user.name = kwargs['name']
        except:
            pass

        try:
            if(kwargs['image_url'] != None):
                exisiting_user.image_url = kwargs['image_url']
        except:
            pass
        

        exisiting_user.save()

        return UpdateUserMutation(user=exisiting_user)



class Mutation(graphene.ObjectType):

    create_user = CreateUserMutation.Field()

    update_user = UpdateUserMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
