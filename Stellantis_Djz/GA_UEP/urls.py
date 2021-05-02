from django.urls import path
#from GA_UEP.views import CrudView
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from .views import *
app_name = "GA_UEP"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    
    path("api/get_réf/", views.get_réf, name='get_réf'),

    path("crud/", CrudView.as_view(), name='crud_ajax'),
    path("crossdock/", CrudCrossDock.as_view(), name='cross_dock'),

    path("crossdock/historique/Search", views.SearchHCD, name='cross_dock_HSearch'),

    path("Magdebord/", CrudMagDebord.as_view(), name='Mag_debord'),
    path("FLC/", CrudFLC.as_view(), name='FLC_A'),
    
    path("update/CD", UpdateAler.as_view(), name="update_CD"),

  

    #
    path("update/CD/Histo", UpdateAlerHisto.as_view(), name="update_CD_Histo"),

    path("update/FLC", UpdateAlerFLC.as_view(), name="update_FLC"),
    
    path("update/DB", UpdateAlerDB.as_view(), name="update_DB"),
    path("create/", CreateCrudInv.as_view(), name='create'),
    path('delete/', DeleteCrudInv.as_view(), name='delete'),
    #path("MagDebord", views.MagDebord, name="MagDebord"),
    #path("CrossDock", views.CrossDock, name="CrossDock"),
    path("Dashboard", views.Dashboard, name="Dashboard"),
    path("Error", views.Error, name="Error"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
