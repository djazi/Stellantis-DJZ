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
    #path("ajouter_inv",views.ajouter_inv,name='ajouter_inv'),
    path("api/get_réf/", views.get_réf, name='get_réf'),

    path("crud/", CrudView.as_view(), name='crud_ajax'),
    path("crossdock/", CrudCrossDock.as_view(), name='cross_dock'),

    path("create/CD", CreateCrudAler.as_view(), name="create_CD"),
    path("create/", CreateCrudInv.as_view(), name='create'),
    path('delete/', DeleteCrudInv.as_view(), name='delete'),





    path("MagDebord", views.MagDebord, name="MagDebord"),
    #path("CrossDock", views.CrossDock, name="CrossDock"),
    path("Dashboard", views.Dashboard, name="Dashboard"),
    path("Error", views.Error, name="Error"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
