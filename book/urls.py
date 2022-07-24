
from django.urls import path, re_path
from book import views

urlpatterns = [

    # livres
    re_path(r'^$', views.BookViewSet.as_view({'get': 'list', 'post': 'post'}), name='list_book'),
    re_path(r'^(?P<id>\d+)$', views.BookDetailViewSet.as_view({'get': 'retrieve', 'put': 'put', 'post': 'put', 'delete': 'delete'}), name="detail_livre"),
    re_path(r'^similars/$', views.SimalarBooksViewSet.as_view({'get': 'list'}), name='list_book'),

    # Livre populaires
    path('populars/', views.PopularBooksViewSet.as_view({'get': 'list'}), name='popular_books'),

    # Catégories
    path('categorie/', views.CategorieViewSet.as_view({'get': 'list', 'post': 'post'}), name="list_categorie"),
    re_path(r'^categorie/(?P<id>\d+)$', views.CategorieDetailViewSet.as_view({'get': 'retrieve', 'put': 'put', 'post': 'put', 'delete': 'delete'}), name="detail_categorie"),

    # Utilisateurs
    re_path(r'^utilisateur/$', views.UtilisateurViewSet.as_view({'get': 'list', 'post': 'post'}), name='list_users'),
    re_path(r'^utilisateur/info/$', views.UserInfo.as_view({'get': 'list',}), name='user_info'),
    re_path(r'^utilisateur/(?P<id>\d+)/', views.UtilisateurDetailViewSet.as_view({'get': 'retrieve', 'post': 'put', 'put': 'put', 'delete': 'delete'}), name='detail_user'),

    # liste des livres d'un utilisateurs
    path('utilisateur/me/', views.BookListForUserViewSet.as_view({'get': 'list',}), name='book_list_user'),
    re_path(r'^filter/$', views.FilterBookViewSet.as_view({'get': 'list',}), name='book_filter_list'),
 

    # Commentaires
    path('commentaire/', views.CommentaireListViewSet.as_view({'get': 'list'}), name='list_comment'),
    re_path(r'^(?P<id_book>\d+)/commentaire/$', views.CommentaireCreateViewSet.as_view({'post': 'post'}), name='create_comment'),

    # Partages
    path('partage/', views.PartageListViewSet.as_view({'get': 'list'}), name='list_partage'),
    re_path(r'^(?P<id_book>\d+)/partage/', views.PartageCreateViewSet.as_view({'post': 'post'}), name='create_partage'),


    # Likes
    path('like/', views.LikesListViewSet.as_view({'get': 'list'}), name='list_like'),
    re_path(r'^(?P<id_book>\d+)/like/$', views.LikesCreateViewSet.as_view({'post': 'post'}), name='create_like'),


    # Téléchargements
    path('telecharge/', views.TelechargeListViewSet.as_view({'get': 'list'}), name='list_telecharge'),
    re_path(r'^(?P<id_book>\d+)/telecharge/$', views.TelechargeCreateViewSet.as_view({'post': 'post', 'delete': 'delete'}), name='create_telecharge'),

]
