from django.contrib import admin
from . models import Alertes, Membership, Inventaire, Map, Stock, MapStock, ESStock
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter
from datetime import date, datetime


# Register your models here.

@admin.register(Map)
class MapAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin):
    list_display = ("Map_Réference", "Designation_Produit", "Map_PDC", "condi",
                    "condiQ", "ligne",  "UA_Appro", "UcTourRef",  "Train", "CVM",
                    "Quai", "Crossdock", "BDL", "Id_Appro", "Nom_Appro", "Prénom_Appro")
    search_fields = ['Map_Réference', 'Designation_Produit',
                     'Nom_Appro',  ]


@admin.register(Stock)
class StockAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin):
    list_display = ("Emplacement_SM", "Reference", "Nb_bacs", "Date_heure",
                    "Travee_debord", "Conditionnement_UC",  "Qt_pieces_UC", "Appro",
                    "Fournisseur", "CMJ", "FDS", "StDate")
    search_fields = ['Emplacement_SM', 'Reference',
                     'Fournisseur', ]


@admin.register(ESStock)
class ESStockAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin):
    list_display = ("Emplacement_SM", "Reference", "Nb_bacs", "Date_heure_entrée",
                    "Travee_debord", "Conditionnement_UC",  "Qt_pieces_UC", "Appro",
                    "Fournisseur", "CMJ", "FDS", "Date_heure_sortie", "ESDate")
    search_fields = ['Emplacement_SM', 'Reference',
                     'Fournisseur', ]


@admin.register(MapStock)
class MapStockAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin):
    list_display = ("M_Reference", "M_Emplacement_SM", "M_Conditionnement_UC", "M_Qt_pieces_UC",
                    "M_Appro", "M_Fournisseur",  "M_CMJ", "M_FDS"
                     )
    search_fields = ['M_Emplacement_SM', 'M_Reference',
                     'M_Fournisseur', ]

@admin.register(Membership)
class MembershipAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin):
    list_display = ("person", "Ru", "Moniteur", "permission")
    search_fields = ['person', 'Moniteur',
                     'Ru', ]
    pass
    
    
@admin.register(Inventaire)
class InventaireAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin):
    list_display = ("Reference", "Nombre_De_Bac",
                    "Zone_De_Kit", "SM_Csc", "Date", "heure", "name", "statut", "SDate")
    list_filter = (
        ('SDate', DateRangeFilter), ('name')
    )
    search_fields = ['Reference', 'Date',
                     'Zone_De_Kit', ]
    

@admin.register(Alertes)
class AlertesAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin):
    list_display = ("Reference", "Nombre_De_Bac",
                    "Zone_De_Kit",
                    "SM_Csc", "Code_condi", "QTe_Uc",
                    "Date", "heure", "Moniteur", "statut",
                    "Commenataire", "HFA", "Shifts",
                    "Groupes", "SDate")
                    
    list_filter = (
        ('SDate', DateRangeFilter), ('SDate', DateTimeRangeFilter),
    )
    search_fields = ['Reference', 'Shifts',
                     'Zone_De_Kit', ]
