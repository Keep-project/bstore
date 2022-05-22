# from django.shortcuts import render


from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

# Importation des models
from .models import Books, Categorie, Utilisateur, Commentaire, \
    Partage, Telecharge, Like

# Importation des serializers
from .serializers import BooksSerializer, CategorieSerializer, \
    UtilisateurSerializer, CommentaireSerializer, PartageSerializer, \
    TelechargeSerializer, LikeSerializer

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


class CategorieDetailViewSet(viewsets.ViewSet):

    #  Methode permettant de trouver une catégorie à partir de son Id
    def get_object(self, id):
        try:
            return Categorie.objects.get(id=id)
        except Categorie.DoesNotExist:
            return False


    # Renvoi l'element correspondant à l'ID reçu
    def retrieve(self, request, id=None, *args, **kwargs):

        categorie = self.get_object(id)
        if categorie:
            serializer = CategorieSerializer(categorie)
            return Response({"succes": True, "status": status.HTTP_200_OK, "categorie": serializer.data}, status=status.HTTP_200_OK)
        
        else:
            return Response({"succes": False, "status": status.HTTP_404_NOT_FOUND, "message": "La catégorie ayant l'id = {0} n'existe pas !".format(id)}, status=status.HTTP_404_NOT_FOUND)
    

    # mise à jour de l'element correspondant à l'ID reçu
    def put(self, request, id=None, *args, **kwargs):
        categorie = self.get_object(id)
        
        if categorie:
            serializer = CategorieSerializer(categorie, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"succes": True, "status": status.HTTP_201_CREATED, "categorie": serializer.data}, status=status.HTTP_201_CREATED)
        
            return Response({"succes": False, "status": status.HTTP_404_NOT_FOUND, "message": "Erreur de mise à jour de la catégorie"}, status=status.HTTP_404_NOT_FOUND)
    
        return Response({"succes": False, "status": status.HTTP_404_NOT_FOUND, "message": "La catégorie ayant l'id = {0} n'existe pas !".format(id)}, status=status.HTTP_404_NOT_FOUND)

    
    # suppression de l'element correspondant à l'ID reçu
    def delete(self, request, id=None, *args, **kwargs):
        categorie = self.get_object(id)
        if categorie:
            categorie.delete()
            return Response({"succes": False, "status": status.HTTP_204_NO_CONTENT, "message": "Catégorie supprimé avec succès!"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"succes": False, "status": status.HTTP_404_NOT_FOUND, "message": "La catégorie ayant l'id = {0} n'existe pas !".format(id)}, status=status.HTTP_404_NOT_FOUND)



class BookViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        books = Books.objects.all()
        serializer = BooksSerializer(books, many=True)
        return Response({'status': status.HTTP_200_OK, 'success': True, 'message': 'Liste des livres','books': serializer.data,},status=status.HTTP_200_OK,)

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
            return Response({'status': status.HTTP_201_CREATED, 'success': False, 'messages': 'Livre créé avec succès','livre': serializer.data}, status=status.HTTP_200_OK)

        return Response({'status': status.HTTP_400_BAD_REQUEST, 'data': serializer.error }, status=status.HTTP_400_BAD_REQUEST)



class BookDetailViewSet(viewsets.ViewSet):
   
    def get_object(self, id):
        try:
            return Books.objects.get(id = id)
        except Books.DoesNotExist:
            return False

    def retrieve(self, request, id=None, *args, **kw):  
        book = self.get_object(id)
        if book:
            serializer = BooksSerializer(book)
            return Response({'success': True, 'status': status.HTTP_200_OK, 'livre': serializer.data })

        return Response({"succes": False, "status": status.HTTP_404_NOT_FOUND, "message": "Le livre ayant l'id = {0} n'existe pas !".format(id)}, status=status.HTTP_404_NOT_FOUND)

            

    def put(self, request, id=None, *args, **kwargs):
        book = self.get_object(id)
        
        if book:
            serializer = BooksSerializer(book, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"succes": True, "status": status.HTTP_201_CREATED, "livre": serializer.data}, status=status.HTTP_201_CREATED)

            return Response({"succes": False, "status": status.HTTP_400_BAD_REQUEST, "message": "Erreur de mise à jour du livre"}, status=status.HTTP_400_BAD_REQUEST)
    
        return Response({"succes": False, "status": status.HTTP_404_NOT_FOUND, "message": "Le livre ayant l'id = {0} n'existe pas !".format(id)}, status=status.HTTP_404_NOT_FOUND)

    

    def delete(self, request, id, *args, **kwargs):
        book = self.get_object(id)
        if book:
            book.delete()
            return Response({"succes": False, "status": status.HTTP_204_NO_CONTENT, "message": "Livre supprimé avec succès!"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"succes": False, "status": status.HTTP_404_NOT_FOUND, "message": "Le livre ayant l'id = {0} n'existe pas !".format(id)}, status=status.HTTP_404_NOT_FOUND)



class UtilisateurViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        
        utilisateurs = Utilisateur.objects.all()
        serializer = UtilisateurSerializer(utilisateurs, many=True)
        return Response({'success': True,'status': status.HTTP_200_OK, 'message':'Liste des Utilisateurs', 'utilisateurs': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data
        data['avatar'] = ""
        if ((len(data.get('username')) >= 4) and (len(data.get('password')) >= 8)):

            user = Utilisateur.objects.create_user(
                username= data.get('username'),
                password= data.get('password'),
                email= data.get('email'),
                avatar= request.FILES.get('avatar'),
                is_active=True,
                is_staff=True,
                is_superuser=  True if data.get('is_superuser') else False,
            )
            
            serializer = UtilisateurSerializer(user)
            return Response({'status': status.HTTP_201_CREATED, 'success': True, 'message': 'Utilisateur enrégistré avec succès', 'user': serializer.data}, status=status.HTTP_201_CREATED)
        
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'success': False, 'message': 'Erreur de création de l\'utilisateur. Paramètres incomplèts !',} ,status=status.HTTP_400_BAD_REQUEST)


class UtilisateurDetailViewSet(viewsets.ViewSet):

    def get_object(self, id):
        try:
            return Utilisateur.objects.get(id = id)
        except Utilisateur.DoesNotExist:
            return False


    def retrieve(self, request, id=None, *args, **kw):  
        user = self.get_object(id)
        if user:
            serializer = UtilisateurSerializer(user)
            return Response({'success': True, 'status': status.HTTP_200_OK, 'livre': serializer.data })

        return Response({"succes": False, "status": status.HTTP_404_NOT_FOUND, "message": "L'utilisateur ayant l'id = {0} n'existe pas !".format(id)}, status=status.HTTP_404_NOT_FOUND)



    def put(self, request, id=None, *args, **kwargs):
        user = self.get_object(id)
        
        if user:
            serializer = UtilisateurSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"succes": True, "status": status.HTTP_201_CREATED, "user": serializer.data}, status=status.HTTP_201_CREATED)

            return Response({"succes": False, "status": status.HTTP_400_BAD_REQUEST, "message": "Erreur de mise à jour de l'utilisateur"}, status=status.HTTP_400_BAD_REQUEST)
    
        return Response({"succes": False, "status": status.HTTP_404_NOT_FOUND, "message": "L'utilisateur ayant l'id = {0} n'existe pas !".format(id)}, status=status.HTTP_404_NOT_FOUND)


    def delete(self, request, id, *args, **kwargs):
        user = self.get_object(id)
        if user:
            user.delete()
            return Response({"succes": False, "status": status.HTTP_204_NO_CONTENT, "message": "L'utilisateur supprimé avec succès!"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"succes": False, "status": status.HTTP_404_NOT_FOUND, "message": "L'utilisateur ayant l'id = {0} n'existe pas !".format(id)}, status=status.HTTP_404_NOT_FOUND)



class CommentaireListViewSet(viewsets.ViewSet):
    def list(self, request, id_book=None, *args, **kwargs):
        commentaire = Commentaire.objects.all()
        serializer = CommentaireSerializer(commentaire, many=True)
        return Response({'success': True,'status': status.HTTP_200_OK, 'message':'Liste des commentaires', 'commentaires': serializer.data}, status=status.HTTP_200_OK)

class CommentaireCreateViewSet(viewsets.ViewSet):

    def post(self, request, id_book=None, *args, **kwargs):

        if id_book != None:
            request.data['book'] = int(id_book)
            request.data['utilisateur'] = request.user.id
            serializer = CommentaireSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': status.HTTP_201_CREATED, 'success': True, 'message': 'Commentaire enrégistré avec succès', 'commentaire': serializer.data}, status=status.HTTP_201_CREATED)
            
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'success': False, 'message': 'Erreur de création du commentaire. Paramètres incomplèts !'} ,status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"succes": False, "status": status.HTTP_404_NOT_FOUND, "message": "Vous ne pouvez faire un commentaire sur un livre inconnu !"}, status=status.HTTP_404_NOT_FOUND)


class PartageListViewSet(viewsets.ViewSet):

    def list(self, request, id_book=None, *args, **kwargs):
        partage = Partage.objects.all()
        serializer = PartageSerializer(partage, many=True)
        return Response({'success': True,'status': status.HTTP_200_OK, 'message':'Liste des partages', 'partage': serializer.data}, status=status.HTTP_200_OK)


class PartageCreateViewSet(viewsets.ViewSet):

    def post(self, request, id_book=None, *args, **kwargs):

        if id_book != None:
            request.data['book'] = int(id_book)
            request.data['utilisateur'] = request.user.id

            serializer = PartageSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': status.HTTP_201_CREATED, 'success': True, 'message': 'Partage enrégistré avec succès', 'partage': serializer.data}, status=status.HTTP_201_CREATED)
            
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'success': False, 'message': 'Erreur lors du partage. Paramètres incomplèts !'} ,status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"succes": False, "status": status.HTTP_404_NOT_FOUND, "message": "Vous ne pouvez partager un livre inconnu !"}, status=status.HTTP_404_NOT_FOUND)

class LikesListViewSet(viewsets.ViewSet):

    def list(self, request, id_book=None, *args, **kwargs):
        like = Like.objects.all()
        serializer = LikeSerializer(like, many=True)
        return Response({'success': True,'status': status.HTTP_200_OK, 'message':'Liste des likes', 'like': serializer.data}, status=status.HTTP_200_OK)


class LikesCreateViewSet(viewsets.ViewSet):

    def post(self, request, id_book=None, *args, **kwargs):

        if id_book != None or request.user.id:
            try:
                old_like =  Like.objects.get(Q(book=int(id_book)) & Q(utilisateur=request.user.id))
                new_like = { 'id': old_like.id, 'utilisateur': old_like.utilisateur.id, 'book': old_like.book.id, 'is_like': not old_like.is_like}
                serializer = LikeSerializer(old_like, data=new_like)
                if old_like.is_like:
                    like = Like.objects.get(id=old_like.id)
                    like.delete()
                    return Response({'status': status.HTTP_201_CREATED, 'success': True, 'message': 'Livre disliker avec succès', 'like': new_like}, status=status.HTTP_201_CREATED)
            
            except Like.DoesNotExist:
                new_like = { 'utilisateur': request.user.id, 'book': id_book, 'is_like': True}
                serializer = LikeSerializer(data=new_like)

            if serializer.is_valid():
                serializer.save()
                return Response({'status': status.HTTP_201_CREATED, 'success': True, 'message': 'Livre liker avec succès', 'like': serializer.data}, status=status.HTTP_201_CREATED)
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'success': False, 'message': "Le livre avec l'id = {0} n'existe pas !".format(id_book)} ,status=status.HTTP_400_BAD_REQUEST)
    
        return Response({"succes": False, "status": status.HTTP_404_NOT_FOUND, "message": "Vous ne pouvez liker/disliker un livre inconnu !"}, status=status.HTTP_404_NOT_FOUND)


class TelechargeListViewSet(viewsets.ViewSet):
    def list(self, request, id_book=None, *args, **kwargs):
        telecharge = Telecharge.objects.all()
        serializer = TelechargeSerializer(telecharge, many=True)
        return Response({'success': True,'status': status.HTTP_200_OK, 'message':'Liste des téléchargements', 'telecharges': serializer.data}, status=status.HTTP_200_OK)

class TelechargeCreateViewSet(viewsets.ViewSet):

    def post(self, request, id_book=None, *args, **kwargs):

        if id_book != None:
            request.data['book'] = int(id_book)
            request.data['utilisateur'] = request.user.id
            serializer = TelechargeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': status.HTTP_201_CREATED, 'success': True, 'message': 'Livre téléchargé avec succès', 'telecharge': serializer.data}, status=status.HTTP_201_CREATED)
            
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'success': False, 'message': 'Erreur lors du téléchargement. Paramètres incomplèts !'} ,status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"succes": False, "status": status.HTTP_404_NOT_FOUND, "message": "Vous ne pouvez télécharger un livre inconnu !"}, status=status.HTTP_404_NOT_FOUND)



