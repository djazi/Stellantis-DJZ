from django.db import models
from django.db.models.fields import CharField, FloatField, IntegerField, TimeField

# Create your models here.




class Map(models.Model):
    Map_Réference = models.CharField(max_length=50,null=True,blank=True)
    Map_PDC = models.CharField(max_length=50, null=True, blank=True)
    condiQ = models.CharField(max_length=50, null=True, blank=True)
    ligne = models.CharField(max_length=50, null=True, blank=True)
    condi = models.CharField(max_length=50, null=True, blank=True)
    UA_Appro = models.CharField(max_length=50, null=True, blank=True)
    UcTourRef = models.CharField(max_length=50,null=True, blank=True)
    Designation_Produit = models.CharField(
        max_length=128, null=True, blank=True)
    Train = models.CharField(max_length=50, null=True, blank=True)
    CVM = models.CharField(max_length=50, null=True, blank=True)

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
    Reference = models.CharField(max_length=50, null=True, blank=True)
    Nombre_De_Bac = models.CharField(max_length=50, null=True, blank=True)
    Zone_De_Kit = models.CharField(max_length=50, null=True, blank=True)
    SM_Csc = models.CharField(max_length=50, null=True, blank=True)
    Date = models.CharField(max_length=50, null=True, blank=True)
    heure = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    statut = models.CharField(max_length=50,null=True,blank=True)
    



    
