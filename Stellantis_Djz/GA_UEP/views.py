from typing import List
from django import template
from django.contrib.auth import authenticate, login, logout
from django.db.models.expressions import When
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
from django.db.models import Q
from django.template import Context, context
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail

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
        c = Inventaire.objects.filter(Date=datetime.now().strftime("%d/%m/%Y"), name=person).count()
        if c == 0:
            k = Inventaire(Reference="--",
                           Nombre_De_Bac="--", Zone_De_Kit="--",
                           SM_Csc="--", Date=datetime.now().strftime("%d/%m/%Y"), heure=now.strftime("%H:%M:%S"), name=person)
            k.save()
        context = super().get_context_data(**kwargs)
        context['invs'] = Inventaire.objects.filter(
            Date=datetime.now().strftime("%d/%m/%Y"), name=person).order_by('-heure')

        return context

class CreateCrudInv(View):
    def get(self,request):
        global nm_input,hc
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
        context['alertes'] = Alertes.objects.filter(
            Q(Date=datetime.now().strftime("%d/%m/%Y"), ) | Q(HFA='....') | Q(HFA=None)).order_by('-Date').order_by('-heure').order_by('Nombre_De_Bac')
        
        context['T_A_NT'] = Alertes.objects.filter(Date=datetime.now().strftime("%d/%m/%Y"),
        statut__in=('FLC', 'Alerte', 'Non_T', 'A_Débord')).count()

        context['Train'] = Alertes.objects.filter(
            statut='Train', Date=datetime.now().strftime("%d/%m/%Y")).count()

        context['Adebord'] = Alertes.objects.filter(
            statut__in=('A_Débord', 'Alerte'), Date=datetime.now().strftime("%d/%m/%Y")).count()

        context['Livré'] = Alertes.objects.filter(
            statut='Livré', Date=datetime.now().strftime("%d/%m/%Y")).count()

        context['AT'] = Alertes.objects.filter(
            statut='A_Tranche', Date=datetime.now().strftime("%d/%m/%Y")).count()
        context['AR'] = Alertes.objects.filter(
            statut='A_Remorque', Date=datetime.now().strftime("%d/%m/%Y")).count()

        context['TA'] = Alertes.objects.filter(
            Date=datetime.now().strftime("%d/%m/%Y")).count()
        context['FLC'] = Alertes.objects.filter(
            statut='FLC', Date=datetime.now().strftime("%d/%m/%Y")).count()
        return context
class UpdateAler(View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        st = request.GET.get('statut', None)
        cmnt = request.GET.get('Commenataire', None)
        shif = request.GET.get('Shifts', None)
        grp = request.GET.get('Groupes', None)
        #h = now.strftime("%H:%M:%S")
        obj = Alertes.objects.get(id=id1)
        obj.statut = st
        obj.Commenataire = cmnt
        obj.Shifts = shif
        obj.Groupes = grp
        if(st == "Livré" or st == "Train" or st == "A_Tranche" or st == "A_Remorque"):
            obj.HFA = datetime.now().strftime("%H:%M:%S")
        else:
            obj.HFA = '....'
        obj.save()
        #reponse pour agent Bord de Kit 
        h= Alertes.objects.filter(id= id1)
        for i in h:
            global réfj
            heurej = i.heure
            réfj = i.Reference
        g = Inventaire.objects.get(heure=heurej, Reference=réfj)
        g.statut=st
        g.save()
        if(st=="FLC"):
            mail()
        alt = {'id': obj.id, 'statut': obj.statut, 
               'Commenataire': obj.Commenataire, 'Shifts': obj.Shifts,
               'Groupes': obj.Groupes,'HFA':obj.HFA }
        data = {
            'alt': alt
            
        }
        return JsonResponse(data)



# crud view pour Cross Dock Historique------------------------------------------------------------------ 
# pour la recherche sur les references Alertes dans l'historique 
def SearchHCD(request):
    #total kpi--------------------------------
    HKpi= Context()
    HKpi['T_A_NT'] = Alertes.objects.filter(
        statut__in=('FLC', 'Alerte', 'Non_T', 'A_Débord')).count()
                                               
    HKpi['Train'] = Alertes.objects.filter(statut='Train').count()
        
    HKpi['Adebord'] = Alertes.objects.filter(
        statut__in=('A_Débord', 'Alerte')).count()

    HKpi['Livré'] = Alertes.objects.filter(statut='Livré').count()

    HKpi['AT'] = Alertes.objects.filter(statut='A_Tranche').count()
        
    HKpi['AR'] = Alertes.objects.filter(statut='A_Remorque').count()
        
    HKpi['TA'] = Alertes.objects.all().count()
    HKpi['FLC'] = Alertes.objects.filter(statut='FLC').count()
    if request.method == 'POST': 
        Hréf = request.POST['Hréf']
        Hdate = request.POST['Hdate']
        if(Hréf==""):
            Hdsearch = Alertes.objects.filter( Date=Hdate )
            HKpiJ = Context()
            HKpiJ['T_A_NT'] = Alertes.objects.filter(Date=Hdate,
                statut__in=('FLC', 'Alerte', 'Non_T', 'A_Débord')).count()
            HKpiJ['Train'] = Alertes.objects.filter(
                Date=Hdate, statut='Train').count()
            HKpiJ['Adebord'] = Alertes.objects.filter(Date=Hdate,
                statut__in=('A_Débord', 'Alerte')).count()
            HKpiJ['Livré'] = Alertes.objects.filter(
                Date=Hdate, statut='Livré').count()
            HKpiJ['AT'] = Alertes.objects.filter(
                Date=Hdate, statut='A_Tranche').count()
            HKpiJ['AR'] = Alertes.objects.filter(
                Date=Hdate, statut='A_Remorque').count()
            HKpiJ['TA'] = Alertes.objects.filter(Date=Hdate).count()
            HKpiJ['FLC'] = Alertes.objects.filter(
                Date=Hdate, statut='FLC').count()

        elif(Hdate==""):
            flux = Map.objects.filter(Map_Réference=Hréf)
            Hdsearch = Alertes.objects.filter(Reference=Hréf)
        else:
            Hdsearch = Alertes.objects.filter(Date=Hdate, Reference=Hréf)
            flux = Map.objects.filter(Map_Réference=Hréf)
        if(Hdsearch and Hréf == ""):
         return render(request, 'CDhistorique.html', {"Hdserch": Hdsearch, "HKpiJ": HKpiJ})
        elif(Hdsearch):
            return render(request, 'CDhistorique.html', {"Hdserch": Hdsearch, "HKpi": HKpi, "flux": flux})

        else:
            msg = "Réfrence ou Date Non Valide"
            return render(request,   'CDhistorique.html', {"msg": msg, "HKpi": HKpi})
            
    return render(request,  'CDhistorique.html', {"HKpi": HKpi})

# update alertes from Historique 

class UpdateAlerHisto(View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        st = request.GET.get('statut', None)
        cmnt = request.GET.get('Commenataire', None)
        shif = request.GET.get('Shifts', None)
        grp = request.GET.get('Groupes', None)
        #h = now.strftime("%H:%M:%S")
        obj = Alertes.objects.get(id=id1)
        obj.statut = st
        obj.Commenataire = cmnt
        obj.Shifts = shif
        obj.Groupes = grp
        if(st == "Livré" or st == "Train" or st == "A_Tranche" or st == "A_Remorque"):
            obj.HFA = datetime.now().strftime("%H:%M:%S")
        else:
            obj.HFA = '....'
        obj.save()
        h = Alertes.objects.filter(id=id1)
        for i in h:
            global réfj
            heurej = i.heure
            réfj = i.Reference
        g = Inventaire.objects.get(heure=heurej, Reference=réfj)
        g.statut = st
        g.save()
        if(st == "FLC"):
            mail()
        alt = {'id': obj.id, 'statut': obj.statut,
               'Commenataire': obj.Commenataire, 'Shifts': obj.Shifts,
               'Groupes': obj.Groupes, 'HFA': obj.HFA}
        data = {
            'alt': alt
        }
        return JsonResponse(data)

        

# crud view pour le Magdebord -----------------------------------------------------------------------------
class CrudMagDebord(TemplateView):
    template_name = 'MagDebord.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['alertesD'] = Alertes.objects.filter(
            Q(Date=today.strftime("%d/%m/%Y"), statut__in=('Alerte', 'A_Débord')) | Q(statut__in=('Alerte', 'A_Débord'))).order_by('-heure')
        return context


class UpdateAlerDB(View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        st = request.GET.get('statut', None)
        cmnt = request.GET.get('Commenataire', None)
        #h = now.strftime("%H:%M:%S")
        obj = Alertes.objects.get(id=id1)
        obj.statut = st
        obj.Commenataire = cmnt
        if(st == "Livré" or st == "Train" or st == "A_Tranche" or st == "A_Remorque"):
            obj.HFA = datetime.now().strftime("%H:%M:%S")
        else:
            obj.HFA = '....'
        obj.save()
        h = Alertes.objects.filter(id=id1)
        for i in h:
            heurej = i.heure
            réfj = i.Reference
        g = Inventaire.objects.get(heure=heurej, Reference=réfj)
        g.statut = st
        g.save()
        alt = {'id': obj.id, 'statut': obj.statut,
               'Commenataire': obj.Commenataire,
                'HFA': obj.HFA}
        data = {
            'alt': alt
        }
        return JsonResponse(data)


# crud view pour le FLC -----------------------------------------------------------------------------
class CrudFLC(TemplateView):
    template_name = 'FLC.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['alertesF'] = Alertes.objects.filter(
            Q(Date=today.strftime("%d/%m/%Y"),statut='FLC') | Q(statut='FLC')).order_by('-heure')
        return context

#Q(Date=datetime.now().strftime("%d/%m/%Y"), ) | Q(HFA='....')).order_by('-heure')
class UpdateAlerFLC(View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        st = request.GET.get('statut', None)
        cmnt = request.GET.get('Commenataire', None)
        #h = now.strftime("%H:%M:%S")
        obj = Alertes.objects.get(id=id1)
        obj.statut = st
        obj.Commenataire = cmnt
        if(st == "Livré" or st == "Train" or st == "A_Tranche" or st == "A_Remorque" or st == "FLC_T"):
            obj.HFA = datetime.now().strftime("%H:%M:%S")
        else:
            obj.HFA = '....'
        obj.save()
        h = Alertes.objects.filter(id=id1)
        for i in h:
            heurej = i.heure
            réfj = i.Reference
        g = Inventaire.objects.get(heure=heurej, Reference=réfj)
        g.statut = st
        g.save()
        alt = {'id': obj.id, 'statut': obj.statut,
               'Commenataire': obj.Commenataire,
               'HFA': obj.HFA}
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

#sending automatique email--------------------------------------------------------------------
def mail():
    subject = 'Mail Automatique FLC '
    message = f'Attention risque arrêt de ligne SUR  la reference: {réfj}.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['adamdjazi@gmail.com',
                       'youssef.kabab@stellantis.com']
    send_mail(subject, message, email_from, recipient_list)
    
    


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




