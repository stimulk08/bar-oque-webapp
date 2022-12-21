from rest_framework.urls import path

from .views import AvailableTimeView, MakeReservationView


urlpatterns = [
    path(
        "available-times/",
        AvailableTimeView.as_view(),
        name="available_times"
    ),
    path(
        "reservations/",
        MakeReservationView.as_view(),
        name="make_reservation"
    )
]
