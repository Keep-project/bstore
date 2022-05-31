from re import T
from django.db import models
from django.contrib.auth.models import User

# from io import BytesIO
# from PIL import Image

# Create your models here.


BASE_URL = 'http://192.168.220.1:8000'

class Utilisateur(User):
    avatar=models.FileField(upload_to='avatar/', blank=True, null=True)

    def __str__(self):
        return "{0}".format(self.username)
    
    def get_avatar_url(self):
        
        if self.avatar:
            return  BASE_URL + self.avatar.url
        
        return BASE_URL + "/media/avatar/photo_2022-05-13_16-56-12_d9wjxh1.jpg"

class Categorie(models.Model):
    libelle= models.CharField(max_length=50)

    def __str__(self):
        return "{0}".format(self.libelle)

class Books(models.Model):
    titre= models.CharField(max_length=255, null=False)
    description= models.CharField(max_length=255)
    nbpages= models.IntegerField(null=False, blank=False)
    image= models.FileField(upload_to='couverture/', blank=False, null=False)
    proprietaire = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, null=True, blank=True)
    langue= models.CharField(max_length=10)
    auteur= models.CharField(max_length=50)
    editeur= models.CharField(max_length=50)
    categorie=models.ForeignKey(Categorie, related_name="books", on_delete=models.CASCADE)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)


    class Meta:
        ordering=('-created_at',)

    def __str__(self):
        return "{0}".format(self.titre)

    def get_absolute_url(self):
        return  "/{0}/".format(self.titre)
    
    def get_image_url(self):
        return BASE_URL + self.image.url

class Like(models.Model):
    utilisateur=models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    book=models.ForeignKey(Books, on_delete=models.CASCADE)
    is_like= models.BooleanField(default=False)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

class Commentaire(models.Model):
    utilisateur=models.ForeignKey(Utilisateur,  on_delete=models.CASCADE)
    book=models.ForeignKey(Books, related_name='commmentaires',on_delete=models.CASCADE)
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
    book=models.ForeignKey(Books, related_name="livres", on_delete=models.CASCADE)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

    class Meta:
        ordering=('-created_at',)

