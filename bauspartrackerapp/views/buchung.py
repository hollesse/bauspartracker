from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import generic

from bauspartrackerapp.models import Buchung


class ListView(LoginRequiredMixin, generic.ListView):
    model = Buchung
    paginate_by = 10  # if pagination is desired

    def get_queryset(self):
        return Buchung.objects.filter(bausparvertrag__id=self.kwargs['bausparvertrag__id']).order_by('datum')


class BuchungCreateForm(forms.ModelForm):
    class Meta:
        model = Buchung
        fields = ['datum', 'betrag', 'art']


class CreateView(LoginRequiredMixin, generic.CreateView):
    model = Buchung
    form_class = BuchungCreateForm

    def form_valid(self, form):
        form.instance.bausparvertrag_id = self.kwargs['bausparvertrag__id']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('buchung_list', kwargs={'bausparvertrag__id': self.kwargs['bausparvertrag__id']})
