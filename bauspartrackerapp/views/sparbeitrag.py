from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import generic

from bauspartrackerapp.models import Sparbeitrag, Bausparvertrag


class ListView(LoginRequiredMixin, generic.ListView):
    model = Sparbeitrag
    paginate_by = 10  # if pagination is desired

    def get_queryset(self):
        return Sparbeitrag.objects.filter(bausparvertrag__id=self.kwargs['bausparvertrag__id']).order_by('erste_buchung')

    def get_context_data(self, ** kwargs):
        context = super().get_context_data(**kwargs)
        context["bausparvertrag"] = Bausparvertrag.objects.get(id=self.kwargs['bausparvertrag__id'])
        return context


class SparbeitragCreateForm(forms.ModelForm):
    class Meta:
        model = Sparbeitrag
        fields = ['betrag', 'erste_buchung', 'letzte_buchung']


class CreateView(LoginRequiredMixin, generic.CreateView):
    model = Sparbeitrag
    form_class = SparbeitragCreateForm

    def form_valid(self, form):
        form.instance.bausparvertrag_id = self.kwargs['bausparvertrag__id']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('sparbeitrag_list', kwargs={'bausparvertrag__id': self.kwargs['bausparvertrag__id']})
