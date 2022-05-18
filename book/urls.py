
from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.home),
    path('listes/', views.home),
]
