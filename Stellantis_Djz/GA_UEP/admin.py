from django.contrib import admin
from . models import Person,Group,Membership,Inventaire,Map
# Register your models here.


class MapAdmin(admin.ModelAdmin):
    list_display = ("Map_Réference", "Designation_Produit", "Map_PDC", "condi",
                    "condiQ", "ligne",  "UA_Appro", "UcTourRef", "Designation_Produit", "Train", "CVM")


class GroupAdmin(admin.ModelAdmin):
    list_display = ("RU","unite")


class PersonAdmin(admin.ModelAdmin):
    list_display = ("name","matricule")


class MembershipAdmin(admin.ModelAdmin):
    list_display = ("person", "Ru", "Moniteur")
    


class InventaireAdmin(admin.ModelAdmin):
    list_display = ("Reference", "Nombre_De_Bac",
                    "Zone_De_Kit", "SM_Csc", "Date", "heure", "name", "statut")


admin.site.register(Map, MapAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Membership, MembershipAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Inventaire, InventaireAdmin)

