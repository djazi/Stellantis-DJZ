from django.db import models
from django.db.models.fields import IntegerField, TimeField

# Create your models here.


class Map(models.Model):
    Map_Réference = models.CharField(max_length=50)
    Map_Zone_Kit = models.CharField(max_length=50)
    condiQ = models.IntegerField()
    Designation_Produit = models.CharField(max_length=128)
    Train = models.CharField(max_length=50)
    nbr_Réf_Famille = models.IntegerField()
    Point_De_consom = models.CharField(max_length=50)


class Person(models.Model):
    name = models.CharField(max_length=50)
    matricule = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Group(models.Model):
    RU = models.CharField(max_length=50)
    unite = models.CharField(max_length=50)
    members = models.ManyToManyField(Person, through='Membership')
    def __str__(self):
        return self.RU


class Membership(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    Ru = models.ForeignKey(Group, on_delete=models.CASCADE)
    Moniteur = models.CharField(max_length=50)
        
class Inventaire(models.Model):
    Reference = models.CharField(max_length=50)
    Nombre_De_Bac = models.IntegerField()
    Zone_De_Kit = models.CharField(max_length=50)
    Moniteur = models.CharField(max_length=50)
    Date = models.DateField()
    heure= models.TimeField()
    



    
