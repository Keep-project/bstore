
from rest_framework import serializers



from .models import Books, Categorie


class CategorieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categorie
        fields = (
            'id',
            'libelle',
        )



class BooksSerializer(serializers.ModelSerializer):

    class Meta:
        model = Books
        fields = (
            'id',
            'titre',
            'description',
            'nbpages',
            'get_image_url',
            'langue',
            'auteur',
            'editeur',
            'created_at',
            'updated_at',
        )