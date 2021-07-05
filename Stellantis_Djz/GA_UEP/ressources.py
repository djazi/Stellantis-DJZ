from import_export import resources
from . models import Alertes, Membership, Inventaire, Map, Stock, MapStock,ESStock
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
class StockResource(resources.ModelResource):
    class Meta:
        model = Stock
class MapStockResource(resources.ModelResource):
    class Meta:
        model = MapStock


class ESStockResource(resources.ModelResource):
    class Meta:
        model = ESStock


      
