from django.db import models
from django.contrib.auth.models import User

# from io import BytesIO
# from PIL import Image

# Create your models here.


BASE_URL = 'http://127.0.0.1:8000'

class Utilisateur(User):
    avartar=models.FileField(upload_to='avatar/', blank=False, null=False)

    def __str__(self):
        return "{0}".format(self.username)
    
    def get_avatar_url(self):
        return BASE_URL + self.avatar.url


class Categorie(models.Model):
    libelle= models.CharField(max_length=50)

    def __str__(self):
        return "{0}".format(self.libelle)



class Books(models.Model):
    titre= models.CharField(max_length=255, null=False)
    description= models.CharField(max_length=255)
    nbpages= models.IntegerField(null=False, blank=False)
    image= models.FileField(upload_to='couverture/', blank=False, null=False)
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






class Commentaire(models.Model):
    utilisateur=models.ForeignKey(Utilisateur,  on_delete=models.CASCADE)
    books=models.ForeignKey(Books, related_name='commmentaires',on_delete=models.CASCADE)
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
    books=models.ForeignKey(Books,on_delete=models.CASCADE)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

    class Meta:
        ordering=('-created_at',)

    

class Telechargement(models.Model):
    utilisateur=models.ForeignKey(Utilisateur, related_name='telechargements',  on_delete=models.CASCADE)
    books=models.ForeignKey(Books, related_name="livres", on_delete=models.CASCADE)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

    class Meta:
        ordering=('-created_at',)


class Likes(models.Model):
    utilisateur=models.ForeignKey(Utilisateur,  on_delete=models.CASCADE)
    books=models.ForeignKey(Books, on_delete=models.CASCADE)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

    class Meta:
        ordering=('-created_at',)
   


