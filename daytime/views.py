from deep_translator import GoogleTranslator
from django.shortcuts import render, redirect
from .models import StartDaytime, ChangeDaytime, FactoryDaytime, GasoilDaytime
from authentication.models import Truck
from factory.models import Factory, Station
from adr.models import Adr
from appspataroV2.tools import change_list_to_text, change_text_to_list, validate_list, convert_date, convert_hour
import datetime

def daytime(request):
    day = datetime.date.today()
    context = {
        'title': day,
    }
    last_start = StartDaytime.objects.filter(driver_name=request.user.get_full_name()).last()
    
    if last_start:
        work_list = []
        work_end = True

        for work in last_start.work:
            work_type = work.get('type')
            work_id = work.get('id')
            
            detail = None
            if work_type == 'factory':
                detail = FactoryDaytime.objects.filter(id=work_id).first()
            elif work_type == 'change':
                detail = ChangeDaytime.objects.filter(id=work_id).first()
            elif work_type == 'gasoil':
                detail = GasoilDaytime.objects.filter(id=work_id).first()
            
            if detail:
                work_list.append(detail)
                work_end = work_end and detail.completed  # Vérifie si tous les travaux sont terminés
        
        context.update({
            'start': last_start,
            'halts': work_list,
            'work_end': work_end,
            'dislodge': last_start.city_end != request.user.city,
        })
    
    return render(request, 'daytime/daytime.html', context)


def create_work(request, work_type):
    last_start = StartDaytime.objects.filter(driver_name=request.user.get_full_name()).last()
    if request.method == "POST":
        # Récupération des données depuis le formulaire HTML
        if work_type == 'start':
            work_data = {
                'driver_name': request.user.get_full_name(),
                'truck': request.POST.get('truck').upper(),
                'trailer': request.POST.get('trailer').upper(),
                'city_start': request.POST.get('city_start').capitalize(),
                'sector': request.POST.get('sector').capitalize(),
                'km_start': int(request.POST.get('km_start')),
                'date_start': convert_date(request.POST.get('date_start')),
                'hour_start': convert_hour(request.POST.get('hour_start')),
            }
        else:
            work_data = {
                'name': request.POST.get('name'),
                'arrival_hour': convert_hour(request.POST.get('arrival_hour')),
                'km_arrival': int(request.POST.get('km_arrival')),
            }

        # Création du travail selon le type
        if work_type == "factory":
            
            # Trouver la dernière remorque chargée ou vide
            load_user = StartDaytime.objects.filter(last_load=True).all() # on obtient tout les camions chargé
            last_load_user = None
            if load_user:
                if last_start.sector == 'Distribution':
                    last_load_user = load_user.get(truck=last_start.truck) # on prend celui dont le camion correspond
                else:
                    last_load_user = load_user.get(driver_name=request.user.get_full_name()) # on prend celui qui correspond au chauffeur
            
            # on regarde dans le travail à quel moment il a été chargé
            km_fill = 0
            km_empty = 0
            if last_load_user:
                for work in last_load_user.work:
                    if work.get('type') == 'factory':
                        fact = FactoryDaytime.objects.get(id=work.get('id'))
                        if fact.weight > 0:
                            km_fill = work_data.get('km_arrival') - fact.km_arrival
                            break
                        if fact.weight <= 0:
                            km_empty = work_data.get('km_arrival') - fact.km_arrival
                            break
                    if work.get('type') == 'change':
                        fact = ChangeDaytime.objects.get(id=work.get('id'))
                        if fact.weight > 0:
                            km_fill = work_data.get('km_arrival') - fact.km_arrival
                            break
                        if fact.weight <= 0:
                            km_empty = work_data.get('km_arrival') - fact.km_arrival
                            break
            else:
                km_empty = work_data.get('km_arrival') - last_start.km_start
                
            # on ajoute dans les données les kilomètres à charge et à vide
            work_data['km_filled'] = km_fill
            work_data['km_emptied'] = km_empty
            
            FactoryDaytime.objects.create(**work_data)
            work = FactoryDaytime.objects.last()
        elif work_type == "change":
            ChangeDaytime.objects.create(**work_data)
            work = ChangeDaytime.objects.last()
        elif work_type == "gasoil":
            GasoilDaytime.objects.create(**work_data)
            work = GasoilDaytime.objects.last()
        elif work_type == 'start':
            StartDaytime.objects.create(**work_data)

        # Ajouter le travail dans la liste de la journée
        if last_start:
            if not work_type == 'start':
                last_start.add_work(work.id, work.formal)
        
        return redirect('daytime')  # Redirection après la création du travail
    
    # Récupération du dernier utilisateur terminé
    last_user_compled = StartDaytime.objects.filter(driver_name=request.user.get_full_name(), completed=True).last()
    trailer = None
    last_trailer = None
    if last_user_compled:
        if validate_list(last_user_compled.trailer) == '+':
            trailer = change_text_to_list(last_user_compled.trailer, ',', '.', False)
            last_trailer = trailer[-1]
        else:
            last_trailer = last_user_compled.trailer[:-1].strip()
    
    # Dénomination des titres de page
    if work_type == "factory":
        title = 'Commencer un arrêt'
        factorys = sorted(
            [factory for factory in Factory.objects.all() if request.user.sector in change_text_to_list(factory.sector, ',', '.', False)],
            key=lambda x: x.name,
        )
    elif work_type == "change":
        title = 'Commencer un changement'
        factorys = sorted(
            [factory for factory in Factory.objects.all() if 'Parking' in change_text_to_list(factory.sector, ',', '.', False)],
            key=lambda x: x.name,
        )
    elif work_type == "gasoil":
        title = 'Commencer un plein'
        factorys = sorted(
            [station for station in Station.objects.all()],
            key=lambda x: x.name,
        )
    elif work_type == 'start':
        title = 'Commencer une journée'
        
    # Contexte pour le formulaire
    context = {
        'gender': work_type,
        'title': title,
        'day': datetime.datetime.now(),
        'trucks': Truck.objects.all(),
        'last_trailer': last_trailer,
        'last_user_compled': last_user_compled if last_user_compled else None,
        'factorys': factorys,
        # Ajouter ici les données nécessaires pour pré-remplir le formulaire
    }
    return render(request, 'daytime/create_work.html', context)


def modify_work():
    pass

def completed_work():
    pass