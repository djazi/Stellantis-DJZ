from django.db import models
from django.db.models.fields import CharField, DateField, FloatField, IntegerField, TimeField

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

    Quai = models.CharField(max_length=50, null=True, blank=True)
    Crossdock = models.CharField(max_length=50, null=True, blank=True)
    BDL = models.CharField(max_length=50, null=True, blank=True)
    Id_Appro = models.CharField(max_length=50, null=True, blank=True)
    Nom_Appro = models.CharField(max_length=50, null=True, blank=True)
    Prénom_Appro = models.CharField(max_length=50, null=True, blank=True)


class Membership(models.Model):
    person = models.CharField(max_length=50)
    Ru = models.CharField(max_length=50)
    Moniteur = models.CharField(max_length=50)
    permission = models.CharField(max_length=50, null=True, blank=True)

class Inventaire(models.Model):
    Reference = models.CharField(max_length=50, null=True, blank=True)
    Nombre_De_Bac = models.CharField(max_length=50, null=True, blank=True)
    Zone_De_Kit = models.CharField(max_length=50, null=True, blank=True)
    SM_Csc = models.CharField(max_length=50, null=True, blank=True)
    Date = models.CharField(max_length=50, null=True, blank=True)
    heure = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    statut = models.CharField(max_length=50,null=True,blank=True)
    SDate = models.DateField(auto_now_add=True,null=True, blank=True)
    

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
    Commenataire = models.CharField(max_length=50, null=True, blank=True)
    HFA = models.CharField(max_length=50, null=True, blank=True)
    Shifts = models.CharField(max_length=50, null=True, blank=True)
    Groupes= models.CharField(max_length=50, null=True, blank=True)
    SDate = models.DateField(auto_now_add=True,null=True, blank=True)
    
#gestion de stock débord 
class Stock(models.Model):
    Emplacement_SM = models.CharField(max_length=50, null=True, blank=True)
    Reference = models.CharField(max_length=50, null=True, blank=True)
    Nb_bacs = models.IntegerField(null=True, blank=True)
    Date_heure = models.CharField(max_length=50, null=True, blank=True)
    Travee_debord = models.CharField(max_length=50, null=True, blank=True)
    Conditionnement_UC = models.CharField(max_length=50, null=True, blank=True)
    Qt_pieces_UC = models.CharField(max_length=50, null=True, blank=True)
    Appro = models.CharField(max_length=50, null=True, blank=True)
    Fournisseur = models.CharField(max_length=50, null=True, blank=True)
    CMJ = models.CharField(max_length=50, null=True, blank=True)
    FDS = models.CharField(max_length=50, null=True, blank=True)
    
    

class MapStock(models.Model):
    M_Emplacement_SM = models.CharField(max_length=50, null=True, blank=True)
    M_Reference = models.CharField(max_length=50, null=True, blank=True)
    M_Conditionnement_UC = models.CharField(max_length=50, null=True, blank=True)
    M_Qt_pieces_UC = models.CharField(max_length=50, null=True, blank=True)
    M_Appro = models.CharField(max_length=50, null=True, blank=True)
    M_Fournisseur = models.CharField(max_length=50, null=True, blank=True)
    M_CMJ = models.CharField(max_length=50, null=True, blank=True)
    M_FDS = models.CharField(max_length=50, null=True, blank=True)


class ESStock(models.Model):
    Emplacement_SM = models.CharField(max_length=50, null=True, blank=True)
    Reference = models.CharField(max_length=50, null=True, blank=True)
    Nb_bacs = models.IntegerField(null=True, blank=True)
    Date_heure_entrée = models.CharField(max_length=50, null=True, blank=True)
    Travee_debord = models.CharField(max_length=50, null=True, blank=True)
    Conditionnement_UC = models.CharField(max_length=50, null=True, blank=True)
    Qt_pieces_UC = models.CharField(max_length=50, null=True, blank=True)
    Appro = models.CharField(max_length=50, null=True, blank=True)
    Fournisseur = models.CharField(max_length=50, null=True, blank=True)
    CMJ = models.CharField(max_length=50, null=True, blank=True)
    FDS = models.CharField(max_length=50, null=True, blank=True)
    Date_heure_sortie = models.CharField(max_length=50, null=True, blank=True)
