from eventplanner import models

from django.contrib.auth import models as auth_models
from rest_framework import serializers


class ValidDateMixin:
    def validate(self, attrs):
        if not self.partial and attrs["end_date"] <= attrs["start_date"]:
            raise serializers.ValidationError("End date has to be later than the start date.")
        return attrs


class EventSerializer(ValidDateMixin, serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    timezone = serializers.ReadOnlyField()
    sessions = serializers.HyperlinkedIdentityField(many=True, view_name="session-detail", read_only=True)

    class Meta:
        model = models.Event
        fields = ["id", "name", "start_date", "end_date", "timezone", "sessions", "owner"]


class SessionSerializer(ValidDateMixin, serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    event = serializers.HyperlinkedRelatedField(
        many=False, view_name="event-detail", queryset=models.Event.objects.all()
    )

    class Meta:
        model = models.Session
        fields = ["id", "name", "start_date", "end_date", "speaker", "owner", "event"]


class UserSerializer(serializers.ModelSerializer):
    sessions = serializers.HyperlinkedIdentityField(many=True, view_name="session-detail", read_only=True)
    events = serializers.HyperlinkedIdentityField(many=True, view_name="event-detail", read_only=True)

    class Meta:
        model = auth_models.User
        fields = ["id", "username", "sessions", "events"]
