from django.contrib.auth import authenticate, login, logout
from . models import *
from django.http import HttpResponseBadRequest, HttpResponseRedirect, Http404, request
from django.urls import reverse
from django.shortcuts import render
from django.db.models import Count
from datetime import datetime, timedelta
from django.core import serializers
from django.http.response import HttpResponse, JsonResponse



# Create your views here.

# data we use ------------------------------------------------------------------------------

#function pour un inventaire -----------------------------------------------------------------------
def ajouter_inv(request):
    
    if request.method == 'POST' and 'ajouter_inv' in request.POST:
        réf_inv = request.POST["réf_inv"]
        nbr_bac = request.POST["nbr_bac_inv"]
        return render(request, 'BordKit.html', {"réf_inv":réf_inv, "nbr_bac": nbr_bac})

        










#login functions-------------------------------------------------------------------------------

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')
        #return HttpResponseRedirect(reverse("login"))
    return render(request,'BordKit.html')
    

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            #return HttpResponseRedirect(reverse("index"))
            return render(request, 'BordKit.html')
        else:
            return render(request, 'login.html', {
                "message": "NOM ou Mot de pass est invalide."
            })
    else:
        return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return render(request, 'login.html', {
        "message": "Merci pour Votre Travail ."
    })

#bord KIt function
def Bord_Kit(request):
    return render(request, 'BordKit.html')
#Cross Dock function
def CrossDock(request):
    return render(request, 'CrossDock.html')

#Magdebord function
def MagDebord(request):
    return render(request, 'MagDebord.html')
# Error function
def Error(request):
    return render(request, 'Error.html')
#Dashboard function 
def Dashboard(request):
    return render(request, 'Dashboard.html')


