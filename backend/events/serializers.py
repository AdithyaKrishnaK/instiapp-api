' Serializers for Event '
from rest_framework import serializers
from events.models import Event

class FollowersMethods:
    ' Helper methods for followers '
    def get_count(self, obj, s):
        return obj.user_event_statuses.filter(status=s).count()

    def get_followers(self, obj, s):
        from users.serializers import UserProfileSerializer
        # pylint: disable=maybe-no-member
        return [UserProfileSerializer(x.user, context=self.context).data \
                for x in obj.user_event_statuses.filter(status=s)]

class EventSerializer(serializers.ModelSerializer):
    '''
    Serializer for Event
    This serializer returns only the count of followers in
    each category, i.e. interested and going and minimal
    venue info. Use `EventFullSerializer` if you want information
    on individual users and venues
    '''

    from locations.serializers import LocationSerializerMin

    interested_count = serializers.SerializerMethodField()
    get_interested_count = lambda self, obj: FollowersMethods.get_count(self, obj, 1)

    going_count = serializers.SerializerMethodField()
    get_going_count = lambda self, obj: FollowersMethods.get_count(self, obj, 2)

    venues = LocationSerializerMin(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ('id', 'name', 'description', 'image_url',
                  'start_time', 'end_time', 'all_day', 'venues', 'bodies',
                  'interested_count', 'going_count')

class EventFullSerializer(serializers.ModelSerializer):
    '''
    Serializer for Event with more information
    Returns the entire list of followers in each category and
    detailed information on venues
    '''

    from bodies.serializers import BodySerializerMin
    from locations.serializers import LocationSerializer
    from locations.models import Location
    from bodies.models import Body

    interested_count = serializers.SerializerMethodField()
    get_interested_count = lambda self, obj: FollowersMethods.get_count(self, obj, 1)

    going_count = serializers.SerializerMethodField()
    get_going_count = lambda self, obj: FollowersMethods.get_count(self, obj, 2)

    interested = serializers.SerializerMethodField()
    get_interested = lambda self, obj: FollowersMethods.get_followers(self, obj, 1)

    going = serializers.SerializerMethodField()
    get_going = lambda self, obj: FollowersMethods.get_followers(self, obj, 2)

    venues = LocationSerializer(many=True, read_only=True)
    venues_id = serializers.PrimaryKeyRelatedField(many=True, read_only=False,
                                                   queryset=Location.objects.all(), source='venues')

    bodies = BodySerializerMin(many=True, read_only=True)
    bodies_id = serializers.PrimaryKeyRelatedField(many=True, read_only=False,
                                                   queryset=Body.objects.all(), source='bodies')

    class Meta:
        model = Event
        fields = ('id', 'name', 'description', 'image_url', 'start_time',
                  'end_time', 'all_day', 'venues', 'venues_id', 'bodies', 'bodies_id',
                  'interested_count', 'going_count', 'interested', 'going')

class UserEventStatusSerializer(serializers.ModelSerializer):

    class Meta:
        from events.models import UserEventStatus
        model = UserEventStatus
        fields = ('id', 'event', 'user', 'status')

class EventLocationSerializer(serializers.ModelSerializer):
    '''
    Gets event with detailed location info
    Intended use with POST list
    '''

    from locations.serializers import LocationSerializer

    venues = LocationSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ('id', 'name', 'venues')