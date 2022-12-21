from django.urls import reverse
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response

from datetime import datetime, time

from collections import deque

from . import serializers
from apps.kabak.models import Reservation, Table

import qrcode


START_TIME = datetime(2001, 1, 7, 10, 0)
END_TIME = datetime(2001, 1, 7, 23, 0)
TIME_SHIFT = time(0, 15)


def convert_time_to_int(str_time):
    split_time = str_time.split(':')
    return int(split_time[0]) * 60 + int(split_time[1])


def convert_datetime_to_int(datetime_time):
    return datetime_time.hour * 60 + datetime_time.minute


def convert_int_time_to_str(int_time):
    hours = int_time // 60
    hours = str(hours).rjust(2, '0')
    minutes = int_time % 60
    minutes = str(minutes).rjust(2, '0')
    return hours + ':' + minutes


class ReservationTime:
    def __init__(self, reservation):
        self.start_time = convert_datetime_to_int(reservation.time)
        self.end_time = self.start_time + \
            convert_datetime_to_int(reservation.duration)


def get_available_times(
    wanted_duration,
    reservations,
):
    start_time = convert_datetime_to_int(START_TIME)
    end_time = convert_datetime_to_int(END_TIME)
    duration = convert_time_to_int(wanted_duration)
    time_shift = convert_datetime_to_int(TIME_SHIFT)
    busy_periods = [
        ReservationTime(reservation) for reservation in reservations
    ]
    busy_periods.sort(key=lambda period: period.start_time)
    busy_periods = deque(busy_periods)

    if not len(busy_periods):
        return fill_empty_period(
            start_time, end_time, duration, time_shift, []
        )

    current_start_time = start_time
    current_end_time = start_time + duration
    result = []
    while current_end_time <= end_time:
        if not len(busy_periods):
            return fill_empty_period(
                current_start_time,
                end_time,
                duration,
                time_shift,
                result
            )

        current_busy_period = busy_periods.popleft()

        if current_busy_period.start_time < current_end_time:
            current_start_time = current_busy_period.end_time
            current_end_time = current_start_time + duration
            continue

        busy_periods.appendleft(current_busy_period)
        result.append(convert_int_time_to_str(current_start_time))
        current_start_time += time_shift
        current_end_time += time_shift

    return result


def fill_empty_period(
    start_time,
    end_time,
    duration,
    time_shift,
    available_times,
):
    current_start_time = start_time
    current_end_time = current_start_time + duration
    while current_end_time <= end_time:
        current_time = convert_int_time_to_str(current_start_time)
        available_times.append(current_time)
        current_start_time += time_shift
        current_end_time += time_shift
    return available_times


class AvailableTimeView(ListAPIView):
    serializer_class = serializers.AvailableTimesSerializer
    queryset = Reservation.objects.none()

    def list(self, request, *args, **kwargs):
        date = request.GET["date"]
        date = datetime.strptime(date, "%Y-%m-%d")
        table = Table.objects.get(number=int(request.GET["table"]))
        reservations = Reservation.objects.filter(
            date=date,
            table=table,
        ).order_by("time")
        wanted_duration = request.GET["duration"]
        available_times = {
            "times": get_available_times(wanted_duration, reservations)
        }
        response_serializer = self.get_serializer(data=available_times)
        response_serializer.is_valid(raise_exception=True)
        return Response(response_serializer.data)


class MakeReservationView(CreateAPIView):
    serializer_class = serializers.ReservationSerializer
    queryset = Reservation.objects.all()
    app_url = "http://127.0.0.1:8000"

    def save_qr_code(self, instance):
        reservation_id = instance.id
        url = self.app_url + reverse(
            "reservation_detail",
            kwargs={"pk": reservation_id}
        )
        img = qrcode.make(url)
        img.save(f"media/qrs/{reservation_id}.png")
        instance.qr_code = f"qrs/{reservation_id}.png"
        instance.save()
        return instance

    def create(self, request, *args, **kwargs):
        table_number = int(request.data["table_id"])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        table_id = Table.objects.get(number=table_number).id
        serializer.save(table_id=table_id)
        self.save_qr_code(serializer.instance)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
