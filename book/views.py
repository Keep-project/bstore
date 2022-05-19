# from django.shortcuts import render


from rest_framework.response import Response
from rest_framework import viewsets, status
import json

# Importation des models
from .models import Books, Categorie

# Importation des serializers
from .serializers import BooksSerializer, CategorieSerializer

# Create your views here.


class CategorieViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        categorie = Categorie.objects.all()
        serializer = CategorieSerializer(categorie, many=True)
        return Response(
            {
                'status': status.HTTP_200_OK,
                'success': True,
                'message': 'Liste des categories',
                'categorie': serializer.data,
            }
            ,status=status.HTTP_200_OK,
        )

    def post(self, request, *args, **kwargs):
        serializer = CategorieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(request.data, status=status.HTTP_200_OK)

        return Response({'status': status.HTTP_400_BAD_REQUEST, 'data': serializer.error }, status=status.HTTP_400_BAD_REQUEST)


class BookViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        books = Books.objects.all()
        serializer = BooksSerializer(books, many=True)
        return Response(
            {
                'status': status.HTTP_200_OK,
                'success': True,
                'message': 'Liste des livres',
                'books': serializer.data,
            }
            ,status=status.HTTP_200_OK,
        )

    def post(self, request, *args, **kwargs):

        request.data['image'] = ""
        serializer = BooksSerializer(data=request.data)
        categorie = Categorie.objects.get(id=request.data.get('categorie'))
        if serializer.is_valid():
            livre = Books(
                titre= request.data.get('titre'),
                description= request.data.get('description'),
                nbpages= request.data.get('nbpages'),
                langue= request.data.get('langue'),
                image= request.FILES.get('image'),
                auteur= request.data.get('auteur'),
                editeur= request.data.get('editeur'),
                categorie = categorie
            )

            livre.save()

            serializer = BooksSerializer(livre)
            return Response({'status': status.HTTP_201_CREATED, 'success': False, 'messages': 'Livre créé avec succès','livre':serializer.data}, status=status.HTTP_200_OK)

        return Response({'status': status.HTTP_400_BAD_REQUEST, 'data': serializer.error }, status=status.HTTP_400_BAD_REQUEST)
