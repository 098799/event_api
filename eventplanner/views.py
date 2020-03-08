from eventplanner import models
from eventplanner import serializers

from django.contrib.auth import models as auth_models
from rest_framework import permissions
from rest_framework import viewsets


class IsAuthenticatedOrReadOnlyMixin:
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class EventViewSet(IsAuthenticatedOrReadOnlyMixin, viewsets.ModelViewSet):
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer


class SessionViewSet(IsAuthenticatedOrReadOnlyMixin, viewsets.ModelViewSet):
    queryset = models.Session.objects.all()
    serializer_class = serializers.SessionSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = auth_models.User.objects.all()
    serializer_class = serializers.UserSerializer
