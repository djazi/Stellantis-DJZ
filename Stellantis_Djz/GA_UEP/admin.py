from django.contrib import admin
from . models import Map,Person,Group,Membership,Inventaire
# Register your models here.


class MapAdmin(admin.ModelAdmin):
    list_display = ("Map_Réference", "Map_Zone_Kit",
                    "condiQ", "Designation_Produit", "Train", "nbr_Réf_Famille","Point_De_consom")


class GroupAdmin(admin.ModelAdmin):
    list_display = ("RU","unite")


class PersonAdmin(admin.ModelAdmin):
    list_display = ("name","matricule")


class MembershipAdmin(admin.ModelAdmin):
    list_display = ("person", "Ru", "Moniteur")
    


class InventaireAdmin(admin.ModelAdmin):
    list_display = ("Reference", "Nombre_De_Bac",
                    "Zone_De_Kit", "Moniteur", "Date", "heure")


admin.site.register(Map, MapAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Membership, MembershipAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Inventaire, InventaireAdmin)

