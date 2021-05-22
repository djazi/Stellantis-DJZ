from django.contrib import admin
from . models import Alertes,Membership,Inventaire,Map
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter


# Register your models here.

@admin.register(Map)
class MapAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin):
    list_display = ("Map_Réference", "Designation_Produit", "Map_PDC", "condi",
                    "condiQ", "ligne",  "UA_Appro", "UcTourRef",  "Train", "CVM",
                    "Quai", "Crossdock", "BDL", "Id_Appro", "Nom_Appro", "Prénom_Appro")




@admin.register(Membership)
class MembershipAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin):
    list_display = ("person", "Ru", "Moniteur")
    pass
    
    
@admin.register(Inventaire)
class InventaireAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin):
    list_display = ("Reference", "Nombre_De_Bac",
                    "Zone_De_Kit", "SM_Csc", "Date", "heure", "name", "statut")
    list_filter = (
        ('Date', DateRangeFilter),('name')
    )
    


@admin.register(Alertes)
class AlertesAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin):
    list_display = ("Reference", "Nombre_De_Bac",
                    "Zone_De_Kit",
                    "SM_Csc", "Code_condi", "QTe_Uc",
                    "Date", "heure", "Moniteur", "statut",
                    "Commenataire", "HFA", "Shifts",
                    "Groupes")
    list_filter = (
        ('Date', DateRangeFilter), ('Date', DateTimeRangeFilter),
    )
  



