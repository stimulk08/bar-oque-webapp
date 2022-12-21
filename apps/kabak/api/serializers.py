from rest_framework import serializers

from apps.kabak.models import Reservation


class AvailableTimesSerializer(serializers.Serializer):
    times = serializers.ListSerializer(
        child=serializers.TimeField(format="%H:%M")
    )


class ReservationSerializer(serializers.ModelSerializer):
    qr_code = serializers.ImageField(read_only=True)

    class Meta:
        model = Reservation
        fields = (
            "client_name",
            "date",
            "time",
            "duration",
            "table_id",
            "qr_code",
        )
