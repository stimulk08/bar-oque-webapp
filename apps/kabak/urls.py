from django.urls import path

from .views import MainView, ReservationView


urlpatterns = [
    path("", MainView.as_view(), name="index"),
    path(
        "reservation/<int:pk>/",
        ReservationView.as_view(),
        name="reservation_detail"
    ),
]
