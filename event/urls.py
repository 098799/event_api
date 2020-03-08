from django.conf import urls as conf_urls
from django.contrib.admin import site
from django import urls


urlpatterns = [
    urls.path("admin/", site.urls),
    urls.path("api-auth/", conf_urls.include("rest_framework.urls")),
    urls.path("", urls.include("eventplanner.urls")),
]
