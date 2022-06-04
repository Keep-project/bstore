from distutils import extension
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
    description= models.TextField()
    nbpages= models.IntegerField(null=False, blank=False)
    image= models.FileField(upload_to='couverture/', blank=False, null=False)
    extension= models.CharField(max_length=50, default='pdf',)
    fichier = models.FileField(upload_to='documents/', blank=True)
    proprietaire = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, null=True, blank=True)
    langue= models.CharField(max_length=10)
    auteur= models.CharField(max_length=50)
    editeur= models.CharField(max_length=50)
    categorie=models.ForeignKey(Categorie, related_name="books", on_delete=models.CASCADE)
    datepub= models.DateTimeField(null=True)
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
        
        return BASE_URL + "/media/avatar/femme-de-pouvoir.jpg"
    
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

