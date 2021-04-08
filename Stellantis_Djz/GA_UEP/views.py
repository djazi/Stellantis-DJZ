from typing import List
from django.contrib.auth import authenticate, login, logout
from . models import Inventaire, Map, Membership,Person,Group
from django.http import HttpResponseBadRequest, HttpResponseRedirect, Http404, request, HttpResponse
from django.urls import reverse
from django.shortcuts import render
from django.db.models import Count
from django.core import serializers
from django.http.response import HttpResponse, JsonResponse
from datetime import date, datetime
from django.http import  JsonResponse
from django.contrib import messages
import json
from django.views.generic import TemplateView, ListView,View
#----------------------------------------------------

# Create your views here.----------------------------------------

# data we use ------------------------------------------------------------------------------------
today = date.today()
now = datetime.now()
map_all = Map.objects.all() # all columns from Map
d1 = today.strftime("%d/%m/%Y") # la date 
n1 = now.strftime("%H:%M:%S")# l'heure
#autocomplete --------------------------------------------------------------------------------------
def get_réf(request):
  if request.is_ajax():
    q = request.GET.get('term', '')
    réfs = Map.objects.filter(Map_Réference__icontains=q)
    results = []
    for pl in réfs:
      réfs_json = {}
      réfs_json = pl.Map_Réference
      results.append(réfs_json)
    data = json.dumps(results)
  else:
    data = 'fail'
  mimetype = 'application/json'
  return HttpResponse(data, mimetype)

#function pour ajouter un inventaire ----------------------------------------------------------------------------
"""def ajouter_inv(request):

    try:
        
        while True:
            if request.method == 'POST' and 'ajouter_inv' in request.POST:
                réf_inv = request.POST["réf_inv"]
                nbr_bac = request.POST["nbr_bac_inv"]
                filt1 = Map.objects.filter(Map_Réference=réf_inv)
                for i in filt1:
                    zkit = i.Map_PDC
                    cvm = i.CVM
                if cvm is None:
                    cvm= "--"
                k = Inventaire(Reference=réf_inv,
                            Nombre_De_Bac=nbr_bac, Zone_De_Kit=zkit,
                            SM_Csc=cvm, Date=d1, heure= n1)
                k.save()
                return render(request, 'BordKit.html', {"réf_inv":réf_inv, 
                                                        "nbr_bac": nbr_bac, "d1": d1, "n1": n1, "zkit": zkit,
                                                        "cvm": cvm})
    except ValueError:
        message = "error"
        return render(request, 'BordKit.html', {"message": message }) Reference
Nombre_De_Bac"""
                                                
#crud view with ajax -----------------------------------------------------------------------


class CrudView(TemplateView):
    template_name = 'BordKit.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['invs'] = Inventaire.objects.all()
        return context

"""def create(request):
    if request.method =='POST':
        réf_inv = request.POST.get('Reference')
        nbr_bac_inv = request.POST.get('Nombre_De_Bac')
        new = Inventaire(Reference=réf_inv, Nombre_De_Bac=nbr_bac_inv)
        new.save()
    return render(request,"Bordkit.html")"""

class CreateCrudInv(View):
    def get(self,request):
        réf_inv = request.GET.get('Reference', None)
        nbr_bac_inv = request.GET.get('Nombre_De_Bac', None)
        filt1 = Map.objects.filter(Map_Réference=réf_inv)
        for i in filt1:
            zkit = i.Map_PDC
            cvm = i.CVM        
        obj = Inventaire.objects.create(
            Reference = réf_inv,
            Nombre_De_Bac = nbr_bac_inv,
            Zone_De_Kit= zkit,
            SM_Csc=cvm,
            Date=d1,
            heure=n1,
            )
        inv = {'id': obj.id, 'Reference': obj.Reference,
                'Nombre_De_Bac': obj.Nombre_De_Bac ,
                'Zone_De_Kit': obj.Zone_De_Kit,
                'SM_Csc':obj.SM_Csc,
                'Date': obj.Date,
                'heure': obj.heure,
                }
        data = {
                'inv':inv
            }
        return JsonResponse(data)


class DeleteCrudInv(View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        Inventaire.objects.get(id=id1).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)

#login functions-------------------------------------------------------------------------------

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')
        #return HttpResponseRedirect(reverse("login"))
    return render(request, 'Dashboard.html')
    

def login_view(request):
    if request.method == "POST":
        global username,user
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            #return HttpResponseRedirect(reverse("index"))
            return render(request, 'Dashboard.html')
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



