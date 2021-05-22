from import_export import resources
from . models import Alertes, Membership, Inventaire, Map


class MembershipResource(resources.ModelResource):
    class Meta:
        model=Membership


class AlertesResource(resources.ModelResource):
    class Meta:
        model = Alertes


class InventaireResource(resources.ModelResource):
    class Meta:
        model = Inventaire


class MapResource(resources.ModelResource):
    class Meta:
        model = Map


      
