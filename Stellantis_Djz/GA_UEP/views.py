from typing import List
from django.contrib.auth import authenticate, login, logout
from . models import Alertes, Inventaire, Map, Membership
from django.http import HttpResponseBadRequest, HttpResponseRedirect, Http404, request, HttpResponse
from django.urls import reverse
from django.shortcuts import render
from django.db.models import Count
from django.core import serializers
from django.http.response import HttpResponse, JsonResponse
from datetime import date, datetime
from django.http import JsonResponse
from django.contrib import messages
import json
from django.views.generic import TemplateView, ListView, View
from django.contrib.sessions.models import Session
#----------------------------------------------------

# Create your views here.----------------------------------------

# data we use ------------------------------------------------------------------------------------
today = date.today()
now = datetime.now()
map_all = Map.objects.all() # all columns from Map
d1 = today.strftime("%d/%m/%Y") # la date 
n1 = now.strftime("%H:%M:%S")# l'heure
#autocomplete  bordkit --------------------------------------------------------------------------------------
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


                                                
#crud  pour Borkit page view with ajax -----------------------------------------------------------------------
class CrudView(TemplateView):
    template_name = 'BordKit.html'
    def get_context_data(self, **kwargs):
        person = self.request.user.username 
        c = Inventaire.objects.filter(Date=d1, name=person).count()
        if c == 0:
            k = Inventaire(Reference="--",
                           Nombre_De_Bac="--", Zone_De_Kit="--",
                           SM_Csc="--", Date=today.strftime("%d/%m/%Y"), heure=now.strftime("%H:%M:%S"), name=person)
            k.save()
        context = super().get_context_data(**kwargs)
        context['invs'] = Inventaire.objects.filter(
            Date=today.strftime("%d/%m/%Y"), name=person)

        return context

class CreateCrudInv(View):
    def get(self,request):
        global nm_input
        réf_inv = request.GET.get('Reference', None)
        nbr_bac_inv = request.GET.get('Nombre_De_Bac', None)

        nm_input = request.GET.get('name', None)

        dc = request.GET.get('Date', None)
        hc = request.GET.get('heure', None)

        filt2 = Inventaire.objects.filter(name=nm_input)
        for j in filt2:
            nm = j.name
       
        filt1 = Map.objects.filter(Map_Réference=réf_inv)
        for i in filt1:
            zkit = i.Map_PDC
            cvm = i.CVM  
            condi = i.condi
            uc = i.condiQ

        #add data to alertes
        
       
        
        obj = Inventaire.objects.create(
            Reference = réf_inv,
            Nombre_De_Bac = nbr_bac_inv,
            Zone_De_Kit= zkit,
            SM_Csc=cvm,
            Date=dc,
            heure=hc,
            name=nm,)
        inv = {'id': obj.id, 'Reference': obj.Reference,
                'Nombre_De_Bac': obj.Nombre_De_Bac,
                'Zone_De_Kit': obj.Zone_De_Kit,
                'SM_Csc':obj.SM_Csc,
                'Date': obj.Date,
                'heure': obj.heure,
                'name': obj.name
                }
        data = {
                'inv':inv
            }
        # convert inventair to alerte
        filt3 = Membership.objects.filter(person=nm_input)
        for j in filt3:
            moniteur = j.Moniteur
        al = Alertes(
            Reference=réf_inv,
            Nombre_De_Bac=nbr_bac_inv,
            Zone_De_Kit=zkit,
            SM_Csc=cvm,
            Code_condi=condi,
            QTe_Uc=uc,
            Date=dc,
            heure=hc,
            Moniteur= moniteur)
        al.save()
        
        return JsonResponse(data)


class DeleteCrudInv(View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        Inventaire.objects.get(id=id1).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)


# crud view pour le crossDock -----------------------------------------------------------------------------
class CrudCrossDock(TemplateView):
    template_name = 'CrossDock.html'
    def get_context_data(self, **kwargs):   
        context = super().get_context_data(**kwargs)
        context['alertes'] = Alertes.objects.all()
        return context




class UpdateAler(View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        st = request.GET.get('statut', None)
        
        cmnt = request.GET.get('Commenataire', None)

        shif = request.GET.get('Shifts', None)
                               
        grp = request.GET.get('Groupes', None)

        obj = Alertes.objects.get(id=id1)
        obj.statut = st
        
        obj.Commenataire = cmnt
        
        obj.Shifts = shif
        obj.Groupes = grp

        obj.save()

        alt = {'id': obj.id, 'statut': obj.statut, 
               'Commenataire': obj.Commenataire, 'Shifts': obj.Shifts,
               'Groupes': obj.Groupes}

        data = {
            'alt': alt
        }
        return JsonResponse(data)















#login functions-------------------------------------------------------------------------------
def index(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')
        #return HttpResponseRedirect(reverse("login"))
    return render(request, 'login.html')


def login_view(request):
    if request.method == "POST":
        global username
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









#bord KIt function-----------------------------------------------------------------------------------
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



