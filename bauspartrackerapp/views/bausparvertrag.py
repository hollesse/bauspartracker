from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import generic

from bauspartrackerapp.models import Bausparvertrag


class ListView(LoginRequiredMixin, generic.ListView):
    model = Bausparvertrag
    ordering = 'id'
    paginate_by = 10  # if pagination is desired

    def get_queryset(self):
        return Bausparvertrag.objects.filter(user=self.request.user).order_by('id')


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Bausparvertrag


class BausparvertragCreateForm(forms.ModelForm):
    class Meta:
        model = Bausparvertrag
        fields = ['bausparkasse',
                  'tarifname',
                  'bausparsumme',
                  'vertragsbeginn',
                  'abschlussgebuehren_prozent',
                  'abschlussgebuehren_in_euro',
                  'laufende_gebuehren_in_euro',
                  'laufende_gebuehren_zeitraum',
                  'zinsen_ansparphase',
                  ]


class CreateView(LoginRequiredMixin, generic.CreateView):
    model = Bausparvertrag
    form_class = BausparvertragCreateForm

    def get_success_url(self):
        return reverse('bausparvertrag_detail', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
