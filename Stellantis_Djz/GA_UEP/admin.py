from django.contrib import admin
from . models import Alertes,Membership,Inventaire,Map
# Register your models here.


class MapAdmin(admin.ModelAdmin):
    list_display = ("Map_Réference", "Designation_Produit", "Map_PDC", "condi",
                    "condiQ", "ligne",  "UA_Appro", "UcTourRef",  "Train", "CVM")




class MembershipAdmin(admin.ModelAdmin):
    list_display = ("person", "Ru", "Moniteur")
    


class InventaireAdmin(admin.ModelAdmin):
    list_display = ("Reference", "Nombre_De_Bac",
                    "Zone_De_Kit", "SM_Csc", "Date", "heure", "name", "statut")


class AlertesAdmin(admin.ModelAdmin):
    list_display = ("Reference", "Nombre_De_Bac",
                    "Zone_De_Kit", 
                    "SM_Csc", "Code_condi", "QTe_Uc",
                    "Date", "heure", "Moniteur", "statut",
                    "Commenataire", "HFA", "Shifts",
                    "Groupes")


admin.site.register(Map, MapAdmin)
admin.site.register(Membership, MembershipAdmin)
admin.site.register(Inventaire, InventaireAdmin)
admin.site.register(Alertes, AlertesAdmin)

