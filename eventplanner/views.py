from eventplanner import models
from eventplanner import serializers

from django.contrib.auth import models as auth_models
from rest_framework import viewsets


class SessionViewSet(viewsets.ModelViewSet):
    queryset = models.Session.objects.all()
    serializer_class = serializers.SessionSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = auth_models.User.objects.all()
    serializer_class = serializers.UserSerializer
