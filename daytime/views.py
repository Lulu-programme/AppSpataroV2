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
    if StartDaytime.objects.filter(name_driver=request.user.get_full_name()).last():
        start = StartDaytime.objects.filter(name_driver=request.user.get_full_name()).last()
        work_list = []
        work_end = True
        for work in start.work:
            work_type = work.get('type')
            work_id = work.get('id')
            if work_type == 'factory':
                detail = FactoryDaytime.objects.get(id=work_id)
            elif work_type == 'change':
                detail = ChangeDaytime.objects.get(id=work_id)
            elif work_type == 'gasoil':
                detail = GasoilDaytime.objects.get(id=work_id)
            else:
                detail = None
                
            if detail:
                work_list.append(detail)
                work_end = True if detail.compled else False
                
        
        context['start'] = start
        context['halts'] = work_list
        context['work_end'] = work_end
        context['dislodge'] = False if start.city_end == request.user.city else True
    
    return render(request, 'daytime/daytime.html', context)

def create_work(request, gender):
    
    start = StartDaytime.objects.filter(name_driver=request.user.get_full_name()).last()
    
    try:
        start_full = StartDaytime.objects.filter(compled=True).all()
    except StartDaytime.objects.filter(compled=True).all().DoesNotExist:
        start_full = None
    
    context = {
        'gender': gender,
        'trucks': Truck.objects.all(),
        'user_truck': str(request.user.truck),
        'day': datetime.datetime.now(),
        'start': start,
    }
    
    if gender == 'start':
        
        # Importation de la class StartDaytime pour la création de l'entrée
        form = StartDaytime.objects.all()
        
        # Récupérer les infos nécésaires et les transmètres des entrées terminées
        if start_full:
            for last in reversed(start_full):
                if last.name_driver == request.user.get_full_name():
                    last_user_compled = last
                    if last.trailer:
                        user_trailer = change_text_to_list(last.trailer, ',', '.', False)
                        last_trailer = user_trailer[-1].upper()
                        context['last_trailer'] = last_trailer
                        break
        else:
            context['last_trailer'] = None
            context['last_user_compled'] = None
        context['title'] = 'Commencer la journée'
        context['last_user_compled'] = last_user_compled
        
        # Récupération des données du formulaire
        if request.method == 'POST':
            name_driver = request.user.get_full_name()
            truck = request.POST.get('truck').upper()
            sector = request.POST.get('sector')
            trailer = request.POST.get('trailer').upper() if sector != 'Distribution' else None
            city_start = request.POST.get('city_start').capitalize()
            date_start = convert_date(request.POST.get('date_start'))
            hour_start = convert_hour(request.POST.get('hour_start'))
            km_start = int(request.POST.get('km_start'))
            
            # Création de l'entrée en fonction du secteur
            try:
                form.create(
                    name_driver=name_driver,
                    truck=truck,
                    trailer=trailer,
                    sector=sector,
                    city_start=city_start,
                    date_start=date_start,
                    hour_start=hour_start,
                    km_start=km_start
                )
            except Exception as e:
                error = GoogleTranslator(source='auto', target='fr').translate(str(e))
                context['error'] = error
            
            return redirect('daytime')            
    
    if gender == 'change':
        
        # Importation de la classe ChangeDaytime pour la création de l'entrée
        form = ChangeDaytime.objects.all()
        
        # Récupérer les infos nécéssaires et les transmètres
        factorys = sorted(
            [
                fac for fac in Factory.objects.all() if 'Parking' in change_text_to_list(fac.sector, ',', '.', False)
            ],
            key=lambda x: x.name
        )
        context['factorys'] = factorys
        context['title'] = 'Commencer un changement'
        
        if request.method == 'POST':
            
            # Récupération des données du formulaire
            name = request.POST.get('name')
            hour_arrival = convert_hour(request.POST.get('hour_arrival'))
            km_arrival = int(request.POST.get('km_arrival'))
            
            try:
                
                # Création de l'entrée
                form.create(
                    name=name,
                    hour_arrival=hour_arrival,
                    km_arrival=km_arrival,
                )
                
                # Ajouter le dernier changement au travail de la journée du chauffeur
                last = ChangeDaytime.objects.last()
                start.add_work(last.id, last.formel)
                
                return redirect('daytime')
                
            except Exception as e:
                error = GoogleTranslator(source='auto', target='fr').translate(str(e))
                context['error'] = error
    
    if gender == 'gasoil':
        
        # Importation de la classe ChangeDaytime pour la création de l'entrée
        form = GasoilDaytime.objects.all()
        
        # Récupérer les infos nécéssaires et les transmètres
        factorys = sorted(
            [
                fac for fac in Station.objects.all()
            ],
            key=lambda x: x.name
        )
        context['factorys'] = factorys
        context['title'] = 'Commencer le plein'
        
        if request.method == 'POST':
            
            # Récupération des données du formulaire
            name = request.POST.get('name')
            hour_arrival = convert_hour(request.POST.get('hour_arrival'))
            km_arrival = int(request.POST.get('km_arrival'))
            
            try:
                
                # Création de l'entrée
                form.create(
                    name=name,
                    hour_arrival=hour_arrival,
                    km_arrival=km_arrival,
                )
                
                # Ajouter le dernier changement au travail de la journée du chauffeur
                last = GasoilDaytime.objects.last()
                start.add_work(last.id, last.formel)
                
                return redirect('daytime')
                
            except Exception as e:
                error = GoogleTranslator(source='auto', target='fr').translate(str(e))
                context['error'] = error
    
    return render(request, 'daytime/create_work.html', context)

def modify_work(request, gender, id):
    
    context = {
        'gender': gender,
    }
    
    return render(request, 'daytime/modify_work.html', context)

def completed_work(request, gender, id):
    
    # Récupération des dernières journées completes et de la journée en court du chauffeur
    start = StartDaytime.objects.filter(name_driver=request.user.get_full_name()).last()
    
    try:
        start_full = StartDaytime.objects.filter(compled=True).all()
    except StartDaytime.objects.filter(compled=True).all().DoesNotExist:
        start_full = None
        
    # Transmètre les données de base
    context = {
        'day': datetime.datetime.now(),
        'gender': gender,
        'start': start,
    }
    
    if gender == 'change':
        
        # Récuperation de l'entrée déjà commencée
        change = ChangeDaytime.objects.get(id=id)
        
        # Importation des données et les transmètres
        context['title'] = 'Terminer le changement'
        context['change'] = change
        
        # Récupération des données du formulaire
        if request.method == 'POST':
            trailer = request.POST.get('trailer').upper()
            condition = request.POST.get('condition')
            lights = request.POST.get('lights')
            tires = request.POST.get('tires')
            wheight = bool(int(request.POST.get('wheight')))
            hour_start = convert_hour(request.POST.get('hour_start'))
            comment = request.POST.get('comment').capitalize()
            
            # Modification de l'entrée
            try:
                change.trailer = trailer
                change.condition = condition
                change.lights = lights
                change.tires = tires
                change.wheight = wheight
                change.comment = comment
                change.hour_start = hour_start
                change.compled = True
                change.save()
                
                # Ajouter la nouvelle remorque dans la liste des de remorques de la journée
                start.add_trailer(trailer)
                
                return redirect('daytime')
            except Exception as e:
                error = GoogleTranslator(source='auto', target='fr').translate(str(e))
                context['error'] = error
    
    if gender == 'gasoil':
        
        # Récuperation de l'entrée déjà commencée
        gasoil = GasoilDaytime.objects.get(id=id)
        
        # Importation des données et les transmètres
        context['title'] = 'Terminer le plein'
        context['gasoil'] = gasoil
        
        # Récupération des données du formulaire
        if request.method == 'POST':
            diesel = int(request.POST.get('diesel'))
            adblue = int(request.POST.get('adblue'))
            hour_start = convert_hour(request.POST.get('hour_start'))
            
            # Modification de l'entrée
            try:
                gasoil.diesel = diesel
                gasoil.adblue = adblue
                gasoil.hour_start = hour_start
                gasoil.compled = True
                gasoil.save()
                
                return redirect('daytime')
            except Exception as e:
                error = GoogleTranslator(source='auto', target='fr').translate(str(e))
                context['error'] = error
    
    return render(request, 'daytime/completed_work.html', context)
