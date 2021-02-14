from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.urls import reverse
from django.views import generic
from datetime import date, timedelta

from bauspartrackerapp.models import Sparbeitrag, SparbeitragJob


class ListView(LoginRequiredMixin, generic.ListView):
    model = SparbeitragJob
    paginate_by = 10  # if pagination is desired

    def get_queryset(self):
        return SparbeitragJob.objects.filter(sparbeitrag__id=self.kwargs['sparbeitrag__id']).order_by('von_datum_inklusive')


class SparbeitragJobCreateForm(forms.ModelForm):
    class Meta:
        model = SparbeitragJob
        fields = []


class CreateView(LoginRequiredMixin, generic.CreateView):
    model = SparbeitragJob
    form_class = SparbeitragJobCreateForm

    def form_valid(self, form):
        sparbeitrag = Sparbeitrag.objects.get(pk = self.kwargs['sparbeitrag__id'])
        form.instance.sparbeitrag = sparbeitrag
        form.instance.status = "GEPLANT"
        try:
            form.instance.von_datum_inklusive = SparbeitragJob.objects\
                .filter(sparbeitrag__id=self.kwargs['sparbeitrag__id'])\
                .filter(status__in=['GEPLANT', 'ERFOLGREICH'])\
                .latest('bis_datum_inklusive').bis_datum_inklusive+timedelta(days=1)
        except ObjectDoesNotExist:
            form.instance.von_datum_inklusive = sparbeitrag.erste_buchung
        form.instance.bis_datum_inklusive = date.today()
        if form.instance.von_datum_inklusive > form.instance.bis_datum_inklusive:
            raise ValidationError(message="Von Datum muss kleiner sein als Bis Datum")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('sparbeitrag_job_list', kwargs={
            'bausparvertrag__id': self.kwargs['bausparvertrag__id'],
            'sparbeitrag__id': self.kwargs['sparbeitrag__id']
        })
