from eventplanner import views

from django import urls
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r"sessions", views.SessionViewSet)
router.register(r"users", views.UserViewSet)

urlpatterns = [urls.path("", urls.include(router.urls))]
