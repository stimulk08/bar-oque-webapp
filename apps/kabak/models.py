from django.db import models


class Table(models.Model):
    number = models.IntegerField(
        verbose_name="Столик",
    )

    class Meta:
        verbose_name = "Столик для заказа"
        verbose_name_plural = "Столики для заказа"

    def __str__(self):
        return f"Столик {self.number}"


class Reservation(models.Model):
    client_name = models.CharField(
        verbose_name="Имя клиента",
        max_length=100,
    )
    table = models.ForeignKey(
        "Table",
        verbose_name="Выбранный столик",
        related_name="reservations",
        on_delete=models.CASCADE,
    )
    date = models.DateField(
        verbose_name="Дата",
    )
    time = models.TimeField(
        verbose_name="Время",
    )
    duration = models.TimeField(
        verbose_name="Продолжительность",
    )
    qr_code = models.ImageField(
        verbose_name="QR code",
        upload_to="qrs",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Бронь"
        verbose_name_plural = "Брони"

    def __str__(self):
        return f"{self.date} - {self.time}: " \
               f"{self.client_name} столик {self.table.number}"
