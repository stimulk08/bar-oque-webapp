from django.urls import reverse_lazy
from django.views import generic

from .models import Table, Reservation


class MainView(generic.TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tables = Table.objects.all()
        context["tables"] = tables
        return context


class ReservationView(generic.DeleteView):
    success_url = reverse_lazy("index")
    template_name = "reservation_detail.html"
    queryset = Reservation.objects.all()
