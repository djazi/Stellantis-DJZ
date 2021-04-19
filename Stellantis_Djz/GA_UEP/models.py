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






class Membership(models.Model):
    person = models.CharField(max_length=50)
    Ru = models.CharField(max_length=50)
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
    

class Alertes(models.Model):
    Reference = models.CharField(max_length=50, null=True, blank=True)
    Nombre_De_Bac = models.CharField(max_length=50, null=True, blank=True)
    Zone_De_Kit = models.CharField(max_length=50, null=True, blank=True)
    SM_Csc = models.CharField(max_length=50, null=True, blank=True)
    Code_condi = models.CharField(max_length=50, null=True, blank=True)
    QTe_Uc = models.CharField(max_length=50, null=True, blank=True)
    Date = models.CharField(max_length=50, null=True, blank=True)
    heure = models.CharField(max_length=50, null=True, blank=True)
    Moniteur = models.CharField(max_length=50, null=True, blank=True)
    statut = models.CharField(max_length=50, null=True, blank=True)
    Anticipation = models.CharField(max_length=50, null=True, blank=True)
    Au_Débord = models.CharField(max_length=50, null=True, blank=True)
    Commenataire = models.CharField(max_length=50, null=True, blank=True)
    HFA = models.CharField(max_length=50, null=True, blank=True)
    Shifts = models.CharField(max_length=50, null=True, blank=True)
    Groupes= models.CharField(max_length=50, null=True, blank=True)
    

    
