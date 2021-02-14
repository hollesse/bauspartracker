from django.urls import path

from . import views
from .views import buchung, bausparvertrag, sparbeitrag, sparbeitrag_job
from .views.index import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('bausparvertrag/', bausparvertrag.ListView.as_view(), name='bausparvertrag_list'),
    path('bausparvertrag/new', bausparvertrag.CreateView.as_view(), name='bausparvertrag_create'),
    path('bausparvertrag/<int:pk>/', bausparvertrag.DetailView.as_view(), name='bausparvertrag_detail'),
    path('bausparvertrag/<int:bausparvertrag__id>/buchung/', buchung.ListView.as_view(), name='buchung_list'),
    path('bausparvertrag/<int:bausparvertrag__id>/buchung/new', buchung.CreateView.as_view(), name='buchung_create'),
    path('bausparvertrag/<int:bausparvertrag__id>/sparbeitrag/', sparbeitrag.ListView.as_view(), name='sparbeitrag_list'),
    path('bausparvertrag/<int:bausparvertrag__id>/sparbeitrag/new', sparbeitrag.CreateView.as_view(), name='sparbeitrag_create'),
    path('bausparvertrag/<int:bausparvertrag__id>/sparbeitrag/<int:sparbeitrag__id>/job/', sparbeitrag_job.ListView.as_view(), name='sparbeitrag_job_list'),
    path('bausparvertrag/<int:bausparvertrag__id>/sparbeitrag/<int:sparbeitrag__id>/job/new', sparbeitrag_job.CreateView.as_view(), name='sparbeitrag_job_create'),
]
