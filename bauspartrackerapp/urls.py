from django.urls import path

from . import views
from .views.IndexView import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index')
]
