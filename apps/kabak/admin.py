from django.contrib import admin

from .models import Table, Reservation


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    pass


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    pass
