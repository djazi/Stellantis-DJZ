from django.urls import path
from . import views
app_name = "GA_UEP"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("ajouter_inv",views.ajouter_inv,name='ajouter_inv' ),

    

    
    path("BordKit", views.Bord_Kit, name="Bord Kit"),
    path("MagDebord", views.MagDebord, name="MagDebord"),
    path("CrossDock", views.CrossDock, name="CrossDock"),
    path("Dashboard", views.Dashboard, name="Dashboard"),
    path("Error", views.Error, name="Error"),
]
