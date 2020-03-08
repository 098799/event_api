from eventplanner import models

from django.contrib.auth import models as auth_models
from rest_framework import serializers


class SessionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = models.Session
        fields = ["id", "name", "start_date", "end_date", "speaker", "owner"]


class UserSerializer(serializers.ModelSerializer):
    sessions = serializers.HyperlinkedIdentityField(many=True, view_name="session-detail", read_only=True)

    class Meta:
        model = auth_models.User
        fields = ["id", "username", "sessions"]
