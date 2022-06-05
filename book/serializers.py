
from rest_framework import serializers
from django.contrib.auth.models import User


from .models import Books, Categorie, Utilisateur, \
    Commentaire, Partage, Telecharge, Like

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = [
            'id',
            'utilisateur',
            'book',
            'is_like',
        ]

class CommentaireSerializer(serializers.ModelSerializer):

    class Meta:
        model = Commentaire
        fields = [
            'id',
            'utilisateur',
            'contenu',
            'created_at',
            'updated_at',
        ]

class BooksSerializer(serializers.ModelSerializer):

    # likes = LikeSerializer(many=True, read_only=True)
    class Meta:
        model = Books
        fields = (
            'id',
            'titre',
            'proprietaire',
            'description',
            'nbpages',
            'get_image_url',
            'get_fichier_url',
            'likes',
            'nbcommentaires',
            'langue',
            'auteur',
            'editeur',
            'datepub',
            'created_at',
            'updated_at',
        )

class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = [
            'id',
            'libelle',
        ]

class CategorieDetailSerializer(serializers.ModelSerializer):
    books = BooksSerializer(many=True, read_only=True)
    class Meta:
        model = Categorie
        fields = [
            'id',
            'libelle',
            'books',
        ]

class UtilisateurSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Utilisateur
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'get_avatar_url',
            'email',
            'is_staff',
            'is_active',
            'last_login',
            'is_superuser',
            'date_joined',
            'user_permissions',
        ]

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'is_staff',
            'is_active',
            'last_login',
            'is_superuser',
            'date_joined',
            'user_permissions',
        ]

class BooksDetailSerializer(serializers.ModelSerializer):
    # books = UtilisateurSerializer(read_only=True)
    commentaires = CommentaireSerializer(many=True, read_only=True)
    class Meta:
        model = Books
        fields = (
            'id',
            'titre',
            'description',
            'nbpages',
            'extension',
            'get_image_url',
            'get_fichier_url',
            'langue',
            'likes',
            'telecharges',
            'commentaires',
            'auteur',
            'editeur',
            'proprietaire',
            'datepub',
            'created_at',
            'updated_at',
        )

class PartageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Partage
        fields = [
            'id',
            'utilisateur',
            'book',
            'created_at',
            'updated_at',
        ]

class TelechargeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Telecharge
        fields = [
            'id',
            'utilisateur',
            'book',
            'created_at',
            'updated_at',
        ]