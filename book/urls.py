
from django.urls import path
from book import views

urlpatterns = [
    path('list/', views.BookViewSet.as_view({'get': 'list', 'post': 'post'})),
    path('list_categorie/', views.CategorieViewSet.as_view({'get': 'list', 'post': 'post'})),
]
