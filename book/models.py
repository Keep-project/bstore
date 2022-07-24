

from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

# Create your models here.

BASE_URL = 'http://192.168.43.100:8000'

# BASE_URL =  'https://bstore-backend.herokuapp.com'

class Utilisateur(User):

    avatar=models.FileField(upload_to='avatars/', blank=True, null=True)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{0}".format(self.username)
    
    def get_avatar_url(self):
        if self.avatar:
            return  BASE_URL + self.avatar.url
        return BASE_URL + "/media/avatar/photo_2022-05-13_16-56-12_d9wjxh1.jpg"


    def get_liked_books(self):
        likes = Like.objects.filter(utilisateur = self.id)
        ids = [like.book_id for like in likes]
        return Books.objects.filter(id__in=ids)
    
    def get_downloads_books(self):
        downloads = Telecharge.objects.filter(utilisateur__id = self.id)
        ids = [download.book_id for download in downloads]
        return Books.objects.filter(id__in=ids)

    def get_uploads_books(self):
        return Books.objects.filter(proprietaire__id = self.id)


class Categorie(models.Model):
    libelle= models.CharField(max_length=50)

    def __str__(self):
        return "{0}".format(self.libelle)


class Books(models.Model):
    
    titre= models.CharField(max_length=255, null=False)
    description= models.TextField()
    nbpages= models.IntegerField(null=False, blank=False)
    image= models.FileField(upload_to='couvertures/', blank=True, null=True)
    extension= models.CharField(max_length=50, default='pdf',)
    fichier = models.FileField(upload_to='documents/', blank=True, null=True)
    proprietaire = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, null=True, blank=True)
    langue= models.CharField(max_length=10)
    auteur= models.CharField(max_length=50)
    editeur= models.CharField(max_length=50)
    categorie=models.ForeignKey(Categorie, related_name="books", on_delete=models.CASCADE)
    datepub= models.CharField( max_length=50, null=True, default="10/03/2022 00:00:00.0")
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

    class Meta:
        ordering=('-created_at',)

    def __str__(self):
        return "{0}".format(self.titre)

    def get_absolute_url(self):
        return  "/{0}/".format(self.titre)
    
    def get_image_url(self):
        if self.image:
            return  BASE_URL + self.image.url
        return BASE_URL + "/media/couvertures/bstore-logo.png"
    
    def get_fichier_url(self):
        if self.fichier:
            return  BASE_URL + self.fichier.url
        return BASE_URL + "/media/documents/photo_2022-04-28_07-10-57.jpg"
    
    def likes(self):
        # return Like.objects.filter(book__id=self.id).count()
        # return self.nblikes.filter(book=self.id).count()
        return self.like_set.filter(book=self.id).count()

    def nbcommentaires(self):
        return self.commentaire_set.filter(book=self.id).count()


    def commentaires(self):
        return self.commentaire_set.filter(book=self.id)

    def telecharges(self):
        return self.telecharge_set.filter(book=self.id).count()

    def get_categorie(self):
        return self.categorie.libelle

class Like(models.Model):
    utilisateur=models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    book=models.ForeignKey(Books, on_delete=models.CASCADE)
    is_like= models.BooleanField(default=False)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

class Commentaire(models.Model):
    utilisateur=models.ForeignKey(Utilisateur,  on_delete=models.CASCADE)
    book=models.ForeignKey(Books, on_delete=models.CASCADE)
    contenu= models.CharField(max_length=255)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

    class Meta:
        ordering=('-created_at',)

    def __str__(self):
        return "{0}".format(self.contenu)

    
    def get_absolute_url(self):
        return  "/{0}/".format(self.contenu)    

class Partage(models.Model):
    utilisateur=models.ForeignKey(Utilisateur,  on_delete=models.CASCADE)
    book=models.ForeignKey(Books,on_delete=models.CASCADE)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

    class Meta:
        ordering=('-created_at',)
    
class Telecharge(models.Model):
    utilisateur=models.ForeignKey(Utilisateur, related_name='telechargements',  on_delete=models.CASCADE)
    book=models.ForeignKey(Books, on_delete=models.CASCADE)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

    class Meta:
        ordering=('-created_at',)
