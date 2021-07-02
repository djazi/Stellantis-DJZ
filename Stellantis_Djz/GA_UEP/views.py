from datetime import timedelta
from typing import List
#from typing_extensions import Annotated
from django import template
from django.contrib.auth import authenticate, login, logout
from django.db.models.aggregates import Max
from django.db.models.base import Model
from django.db.models.expressions import When
from . models import Alertes, Inventaire, Map, MapStock, Membership, Stock
from django.http import HttpResponseBadRequest, HttpResponseRedirect, Http404, request, HttpResponse
from django.urls import reverse
from django.db.models import Count, query
from django.core import serializers
from django.http.response import HttpResponse, JsonResponse
from datetime import date, datetime, timedelta
from django.http import JsonResponse
from django.contrib import messages
import json
from django.views.generic import TemplateView, ListView, View
from django.contrib.sessions.models import Session
from django.db.models import Q, F, DurationField, ExpressionWrapper, Avg, FloatField
from django.template import Context, context
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.db.models.functions import TruncDate
from django.utils.dateparse import parse_datetime
import statistics
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import StockForm
from django.shortcuts import render, redirect


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
                           SM_Csc="--", Date=datetime.now().strftime("%d/%m/%Y"), heure=now.strftime("%H:%M:%S"), name=person, SDate=datetime.now())
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
        if not filt1:
            msg="Réference Non Trouvé"
            data={'msg':msg}
            return JsonResponse(data)
        else:
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
                name=nm,
                )
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
        # convert inventaire to alerte
        if filt1:
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
                Moniteur= moniteur,
                )
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
            Q(Date=datetime.now().strftime("%d/%m/%Y"), ) | Q(HFA='....') | Q(HFA=None)).order_by('-heure')
        context['T_A_NT'] = Alertes.objects.filter(
            Q(Date=datetime.now().strftime("%d/%m/%Y")) & (Q(statut='Alerte_CK')
            | Q(statut=None))).count()
        context['Train'] = Alertes.objects.filter(
            statut='Train', Date=datetime.now().strftime("%d/%m/%Y")).count()
        context['Adebord'] = Alertes.objects.filter(
            statut__in=('A_Débord', 'Alerte_DEB'), Date=datetime.now().strftime("%d/%m/%Y")).count()
        context['Livré'] = Alertes.objects.filter(
            statut='Livré', Date=datetime.now().strftime("%d/%m/%Y")).count()
        context['AT'] = Alertes.objects.filter(
            statut='A_Tranche', Date=datetime.now().strftime("%d/%m/%Y")).count()
        context['AR'] = Alertes.objects.filter(
            statut='A_Remorque', Date=datetime.now().strftime("%d/%m/%Y")).count()

        context['TA'] = Alertes.objects.exclude(statut='Train').filter(                                                                    
            Date=datetime.now().strftime("%d/%m/%Y")).count()

        context['FLC'] = Alertes.objects.filter(
            statut='FLC', Date=datetime.now().strftime("%d/%m/%Y")).count()
        context['FLC_T'] = Alertes.objects.filter(
            statut='FLC_T', Date=datetime.now().strftime("%d/%m/%Y")).count()
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
        (Q(statut='Alerte_CK') | Q(statut=None))).count()
            
                                               
    HKpi['Train'] = Alertes.objects.filter(statut='Train').count()
        
    HKpi['Adebord'] = Alertes.objects.filter(
        statut__in=('A_Débord', 'Alerte_DEB')).count()

    HKpi['Livré'] = Alertes.objects.filter(statut='Livré').count()

    HKpi['AT'] = Alertes.objects.filter(statut='A_Tranche').count()
        
    HKpi['AR'] = Alertes.objects.filter(statut='A_Remorque').count()
        
    HKpi['TA'] = Alertes.objects.filter(statut__in=('Alerte_CK', 'A_Débord', 'Alerte_DEB',
                                                    'Livré', 'A_Tranche', 'A_Remorque', 'FLC', 'FLC_T')
                                        ).count()
    HKpi['FLC'] = Alertes.objects.filter(statut='FLC').count()
    HKpi['FLC_T'] = Alertes.objects.filter(statut='FLC_T').count()


    if request.method == 'POST': 
        Hréf = request.POST['Hréf']
        Hdate = request.POST['Hdate']
        if(Hréf==""):
            Hdsearch = Alertes.objects.filter( Date=Hdate )
            HKpiJ = Context()
            HKpiJ['T_A_NT'] = Alertes.objects.filter(Q(Date=Hdate) & 
            (Q(statut='Alerte_CK') | Q(statut=None))).count()
                                                     
            HKpiJ['Train'] = Alertes.objects.filter(
                Date=Hdate, statut='Train').count()
            HKpiJ['Adebord'] = Alertes.objects.filter(Date=Hdate,
                                                      statut__in=('A_Débord', 'Alerte_DEB')).count()
            HKpiJ['Livré'] = Alertes.objects.filter(
                Date=Hdate, statut='Livré').count()
            HKpiJ['AT'] = Alertes.objects.filter(
                Date=Hdate, statut='A_Tranche').count()
            HKpiJ['AR'] = Alertes.objects.filter(
                Date=Hdate, statut='A_Remorque').count()

            HKpiJ['TA'] = Alertes.objects.exclude(statut='Train').filter(                                                                    
                Date=Hdate).count()
                                                 
            HKpiJ['FLC'] = Alertes.objects.filter(
                Date=Hdate, statut='FLC').count()

            HKpiJ['FLC_T'] = Alertes.objects.filter(
                Date=Hdate, statut='FLC_T').count()

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
            Q(Date=today.strftime("%d/%m/%Y"), statut__in=('Alerte_DEB', 'A_Débord')) | Q(statut__in=('Alerte_DEB', 'A_Débord'))).order_by('-heure')
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
    return render(request, 'home.html')


def login_view(request):
    if request.method == "POST":
        global username
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            #return HttpResponseRedirect(reverse("index"))
            return render(request, 'home.html')
        else:
            return render(request, 'login.html', {
                "message": "NOM ou Mot de pass est invalide."
            })
    else:
        if  request.user.is_authenticated:
            return render(request, 'home.html')
        
def logout_view(request):
    logout(request)
    return render(request, 'login.html', {
        "message": "Merci pour Votre Travail ."
    })

#sending automatique email--------------------------------------------------------------------
#bord KIt function-----------------------------------------------------------------------------------
def Bord_Kit(request):
    return render(request, 'BordKit.html')
#Cross Dock function
def CrossDock(request):
    return render(request, 'CrossDock.html')

#Magdebord function
def MagDebord(request):
    return render(request, 'MagDebord.html')

def GestionStock(request):
    return render(request, 'GestionStock.html' )
# Error function
def Error(request):
    return render(request, 'Error.html')
#Dashboard function 
def Dashboard(request):
    return render(request, 'Dashboard.html')

#Dashboard KPI

class KPIS(TemplateView):
    template_name = 'Dashboard.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    #Doughnut alertes Data--------------------------------------------------------------------------------------------
        context['alertCK'] = Alertes.objects.filter(Date=datetime.now().strftime("%d/%m/%Y"),
            statut__in=('Alerte_CK')).count()
        context['anticipations'] = Alertes.objects.filter(Date=datetime.now().strftime("%d/%m/%Y"),
            statut__in=( 'A_Tranche', 'A_Remorque',)).count()
        context['alertDébord'] = Alertes.objects.filter(Date=datetime.now().strftime("%d/%m/%Y"),
             statut__in=('A_Débord', 'Alerte_DEB',)).count()
        context['FLC'] = Alertes.objects.filter(
            statut='FLC', Date=datetime.now().strftime("%d/%m/%Y")).count()
        context['Train'] = Alertes.objects.filter(
            statut='Train', Date=datetime.now().strftime("%d/%m/%Y")).count()
        context['Livré'] = Alertes.objects.filter(
            statut='Livré', Date=datetime.now().strftime("%d/%m/%Y")).count()

        context['KPO'] = Alertes.objects.filter(Date=datetime.now().strftime("%d/%m/%Y"),
            Zone_De_Kit__startswith ='KPO').count()
        context['KHM'] = Alertes.objects.filter(Date=datetime.now().strftime("%d/%m/%Y"),
            Zone_De_Kit__startswith ='KHM').count()
        context['KH1'] = Alertes.objects.filter(Date=datetime.now().strftime("%d/%m/%Y"),
            Zone_De_Kit__startswith ='KH1').count()
        context['KH2'] = Alertes.objects.filter(Date=datetime.now().strftime("%d/%m/%Y"),
            Zone_De_Kit__startswith ='KH2').count()
        context['KK7'] = Alertes.objects.filter(Date=datetime.now().strftime("%d/%m/%Y"),
            Zone_De_Kit__startswith ='KK7').count()
        context['MV2'] = Alertes.objects.filter(Date=datetime.now().strftime("%d/%m/%Y"),
            Zone_De_Kit__startswith ='KV2').count()
        context['MV34'] = Alertes.objects.filter(Date=datetime.now().strftime("%d/%m/%Y"),
            Zone_De_Kit__startswith ='KMVK').count()
        context['PCI'] = Alertes.objects.filter(Date=datetime.now().strftime("%d/%m/%Y"),
            Zone_De_Kit__startswith ='KPCV').count()
        context['POM'] = Alertes.objects.filter(Date=datetime.now().strftime("%d/%m/%Y"),
            Zone_De_Kit__startswith ='KPM').count()
        context['PSP'] = Alertes.objects.filter(Date=datetime.now().strftime("%d/%m/%Y"),
            Zone_De_Kit__startswith ='KPST').count()
        context['KTB'] = Alertes.objects.filter(Date=datetime.now().strftime("%d/%m/%Y"),
            Zone_De_Kit__startswith ='KTBG').count()
        c = Alertes.objects.filter(statut__in=('Livré','Train','FLC_T','A_Tranche','A_Remorque'), Date=datetime.now().strftime("%d/%m/%Y"))
        datetimeFormat = '%H:%M:%S'
        l=[]
        for i in c:
            h= i.heure
            hf=i.HFA
            diff = abs(datetime.strptime(h, datetimeFormat)
                       - datetime.strptime(hf, datetimeFormat))
            l.append(round(diff.seconds/60,1))
        average = round(Average(l),1)
        context['TAlertes'] = average
        a = Alertes.objects.filter(
            Nombre_De_Bac='2', Date=datetime.now().strftime("%d/%m/%Y")).count()
        b = Alertes.objects.filter(Date=datetime.now().strftime("%d/%m/%Y")).count()
        if b != 0:
            remont = round(((a*100)/b),2)
        else: remont=0
        context['RAlertes'] = remont

        
        return context
#barchart suivi des alertes Data------------------------------------------------------------------------------------------

def suiviAlertes(request):
    dates=[]
    valeures=[]
    queryset = Alertes.objects.filter(SDate__gte=datetime.now()-timedelta(days=8),
        statut__in=('Alerte_DEB', 'A_Débord', 'FLC', 'A_Remorque', 'A_Tranche', 'Livré', 'Alerte_CK', 'FLC_T')
        ).annotate(Dates=TruncDate('SDate') ).values('Date').annotate(Reference=Count('Reference')
        ).values('Reference', 'Date').order_by('SDate' )
    for i in queryset:
        valeures.append(i['Reference'])
        dates.append(i['Date'])
    return JsonResponse(data={
        'dates':dates,
        'valeures':valeures,
    })

def evolutionAlertes(request):
    dates=[]
    antici=[]
    livré=[]
    train=[]
    flct=[]
    queryset = Alertes.objects.filter(SDate__gte=datetime.now()-timedelta(days=8)
    ).annotate(Dates=TruncDate('SDate')).values('Date').annotate(
        liv=Count('statut',filter=Q(statut='Livré')),
        anticip=Count('statut', filter=Q(statut__in=('A_Remorque', 'A_Tranche'))),
        tr=Count('statut', filter=Q(statut='Train')),
        ft=Count('statut', filter=Q(statut='FLC_T')),
    ).values('Date', 'liv', 'anticip','tr','ft').order_by('SDate')
    for i in queryset:
        dates.append(i['Date'])
        livré.append(i['liv'])
        antici.append(i['anticip'])
        train.append(i['tr'])
        flct.append(i['ft'])
    return JsonResponse(data={
        'dates': dates,
        'antici': antici,
        'livré': livré,
        'train': train,
        'flct': flct,
    })

def Top10Alertes(request):
    réf=[]
    fhz=[]
    queryset = Alertes.objects.filter(SDate__gte=datetime.now()-timedelta(days=7)).values(
        'Reference').annotate(fhz=Count('Reference')).order_by('-fhz')[:10]
    for i in queryset:
        réf.insert(0,i['Reference'])
        fhz.insert(0,i['fhz'])
       
    return JsonResponse(data={
        'réf': réf,
        'fhz': fhz,
    })


def Average(lst):
    if sum(lst) ==0 and len(lst)==0:
        return 0
    return sum(lst) / len(lst)

#gestion stock débord---------------------------------------------------------

#autocomplete
def get_réfS(request):
  if request.is_ajax():
    q = request.GET.get('term', '')
    réfs = MapStock.objects.filter(M_Reference__icontains=q)
    results = []
    for pl in réfs:
      réfs_json = {}
      réfs_json = pl.M_Reference
      results.append(réfs_json)
    data = json.dumps(results)
  else:
    data = 'fail'
  mimetype = 'application/json'
  return HttpResponse(data, mimetype)


def get_réfT(request):
  if request.is_ajax():
    q = request.GET.get('term', '')
    réfs = Stock.objects.filter(Travee_debord__icontains=q)
    results = []
    for pl in réfs:
      réfs_json = {}
      réfs_json = pl.Travee_debord
      results.append(réfs_json)
    data = json.dumps(results)
  else:
    data = 'fail'
  mimetype = 'application/json'
  return HttpResponse(data, mimetype)

#stock crud 
class CrudStock(ListView):
    model = Stock
    template_name = 'GestionStock.html'
    context_object_name = 'stocks'
    paginate_by = 10
    queryset = Stock.objects.all().order_by('-Date_heure')


def search_items(request):
    if request.method == 'POST':
        search_str=json.loads(request.body).get('searchText')
        items = Stock.objects.filter(Emplacement_SM__istartswith=search_str) | Stock.objects.filter(
            Reference__istartswith=search_str)
        data = items.values() 
        return JsonResponse(list(data),safe=False)
        
        
class ajouteritem(View):
    def get(self, request):
        ajréf = request.GET.get('ajréf', None)
        ajBac = request.GET.get('ajBac', None)
        ajT = request.GET.get('ajT', None)
        filt1 = MapStock.objects.filter(M_Reference=ajréf)
        if not filt1:
            msg="Réference Non Trouvé"
            data={'msg':msg}
            return JsonResponse(data)
        else:
            for i in filt1:
                M_Emplacement_SM = i.M_Emplacement_SM
                M_Conditionnement_UC = i.M_Conditionnement_UC
                M_Qt_pieces_UC = i.M_Qt_pieces_UC
                M_Appro = i.M_Appro
                M_Fournisseurc = i.M_Fournisseur
                M_CMJ = i.M_CMJ
                M_FDS = i.M_FDS
                #add data to Stock
            Stock.objects.create(
            Emplacement_SM=M_Emplacement_SM,
            Reference=ajréf,
            Nb_bacs=ajBac,
            Date_heure=datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
            Travee_debord=ajT,
            Conditionnement_UC=M_Conditionnement_UC,
            Qt_pieces_UC=M_Qt_pieces_UC,
            Appro=M_Appro,
            Fournisseur=M_Fournisseurc,
            CMJ=M_CMJ,
            FDS=M_FDS,)
            msgy = "Réference ajoutée"
            data = {'msgy': msgy}
          
        return JsonResponse(data)
        
   
class updateitems(View):
    def get(self, request):
        id1 = request.GET.get('idInput', None)
        Nb_bacs = request.GET.get('Nb_bacs', None)
        obj = Stock.objects.get(id=id1)
        obj.Nb_bacs = Nb_bacs
        obj.save()

        alt = {'idInput': obj.id, 'Nb_bacs': obj.Nb_bacs}
        data = {
            'alt': alt
        }
        return JsonResponse(data)
