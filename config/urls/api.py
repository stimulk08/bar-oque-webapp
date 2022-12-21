from django.urls import path, include


urlpatterns = [
    path("kabak/", include("apps.kabak.api.urls")),
]
