from deep_translator import GoogleTranslator
from django.shortcuts import render, redirect
from .models import StartDaytime, ChangeDaytime, FactoryDaytime, GasoilDaytime
from authentication.models import Truck
from factory.models import Factory, Station
from appspataroV2.tools import change_list_to_text, change_text_to_list
import datetime

def daytime(request):
    day = datetime.date.today()
    context = {
        'title': day,
    }
    if StartDaytime.objects.filter(name_driver=request.user.get_full_name()).last():
        start = StartDaytime.objects.filter(name_driver=request.user.get_full_name()).last()
        work_list = []
        
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
        
        context['start'] = start
        context['halts'] = work_list
        context['dislodge'] = False if start.city_end == request.user.city else True
    
    return render(request, 'daytime/daytime.html', context)

def create_work(request, gender):
    context = {
        'trucks': Truck.objects.all(),
        'day': datetime.datetime.now(),
        'user_truck': str(request.user.truck),
        'gender': gender,
    }
    
    if gender == 'start':
        start = StartDaytime.objects.all()
        context['title'] = 'Commencer la journée'
        context['object'] = StartDaytime.objects.last()
        if request.method == 'POST':
            name_driver = request.user.get_full_name() 
            truck = request.POST.getlist('truck')
            trailer = request.POST.get('trailer')
            sector = request.POST.getlist('sector')
            city_start = request.POST.get('city_start')
            date_start = request.POST.get('date_start')
            hour_start = request.POST.get('hour_start')
            km_start = request.POST.get('km_start')

            # Conversion des dates
            date_start_date = datetime.datetime.strptime(date_start, '%Y-%m-%d') if date_start else None
            hour_start_hour = datetime.datetime.strptime(hour_start, '%H:%M') if hour_start else None
            
            start.create(
                name_driver=name_driver,
                truck=change_list_to_text(truck, '.'),
                trailer=trailer.upper(),
                sector=change_list_to_text(sector, '.'),
                city_start=city_start.capitalize(),
                date_start=date_start_date,
                hour_start=hour_start_hour,
                km_start=km_start,
            )
            return redirect('daytime')
        
    if gender == 'factory':
        start = StartDaytime.objects.filter(name_driver=request.user.get_full_name()).last()
        start_list = change_text_to_list(start.sector, '.')
        factorys = sorted(
            [fac for fac in Factory.objects.all() if any(i in change_text_to_list(fac.sector, '.') for i in start_list)],
            key=lambda x: x.name  # Trie par le champ 'name' ou autre critère
        )
        form = FactoryDaytime.objects.all()
        context['factorys'] = factorys
        context['title'] = 'Ajouter un arrêt'
        
        if request.method == 'POST':
            name = request.POST.get('name')
            hour_arrival = request.POST.get('hour_arrival')
            km_arrival = request.POST.get('km_arrival')

            try:
                hour_arrival_hour = datetime.datetime.strptime(hour_arrival, '%H:%M') if hour_arrival else None
                km_arrival = int(km_arrival) if km_arrival else 0
            except ValueError:
                context['error'] = "Heure ou kilométrage invalide."
                return render(request, 'daytime/create_work.html', context)

            # Retrouver la dernière remorque chargée ou vide
            start_last = StartDaytime.objects.filter(name_driver=request.user.get_full_name()).order_by('-id')
            last_km = None
            filled = None

            for entry in start_last:
                if last_km is not None:  # On arrête la recherche dès que `last_km` a une valeur
                    break

                if entry.work:  # Vérifie que `work` n'est pas vide ou None
                    for w in reversed(entry.work):  # Parcours inverse de `work`
                        try:
                            if w.get('type') == 'factory':
                                fact = FactoryDaytime.objects.get(id=w.get('id'))
                                last_km = fact.km_arrival
                                filled = bool(fact.wheight)
                                break
                            elif w.get('type') == 'change':
                                change = ChangeDaytime.objects.get(id=w.get('id'))
                                last_km = change.km_arrival
                                filled = bool(change.wheight)  # Boolean déjà dans la table
                                break
                        except FactoryDaytime.DoesNotExist:
                            context['error'] = f"FactoryDaytime introuvable pour ID {w.get('id')}."
                        except ChangeDaytime.DoesNotExist:
                            context['error'] = f"ChangeDaytime introuvable pour ID {w.get('id')}."

            # Calcul des distances
            km_empty = 0
            km_filled = 0

            # Vérifie les valeurs avant les calculs
            try:
                km_arrival = int(km_arrival)  # Assure que km_arrival est un entier
            except ValueError:
                km_arrival = 0  # Ou une valeur par défaut

            # Calcul des distances
            if last_km is not None:  # Si last_km est défini
                if filled:
                    km_filled = km_arrival - last_km
                else:
                    km_empty = km_arrival - last_km
            else:  # Si last_km est None
                if hasattr(start, 'km_start') and start.km_start is not None:  # Vérifie si start.km_start existe
                    km_empty = km_arrival - start.km_start
                else:
                    km_empty = 0  # Valeur par défaut si aucune distance n'est définie

            # Logs pour vérifier les calculs
            print("Last km:", last_km, "Km empty:", km_empty, "Km filled:", km_filled, 'km arrival:', km_arrival)

            # Création de l'entrée
            try:
                form.create(
                    name=name,
                    hour_arrival=hour_arrival_hour,
                    km_arrival=km_arrival,
                    km_empty=km_empty,
                    km_filled=km_filled,
                )

                last = FactoryDaytime.objects.last()

                start_last[0].add_work(last.id, last.formel)

                return redirect('daytime')
            except Exception as e:
                error = GoogleTranslator(source='auto', target='fr').translate(str(e))
                context['error'] = f"Erreur lors de la création : {error}"
    
    if gender == 'change':
        factorys = sorted(
            [fac for fac in Factory.objects.all() if 'Parking' in change_text_to_list(fac.sector, '.')],
            key=lambda x: x.name  # Trie par le champ 'name' ou autre critère
        )
        start = StartDaytime.objects.filter(name_driver=request.user.get_full_name()).last()
        form = ChangeDaytime.objects.all()
        context['factorys'] = factorys
        context['title'] = 'Changement de remorque'
        
        if request.method == 'POST':
            name = request.POST.get('name')
            hour_arrival = request.POST.get('hour_arrival')
            km_arrival = request.POST.get('km_arrival')

            try:
                hour_arrival_hour = datetime.datetime.strptime(hour_arrival, '%H:%M') if hour_arrival else None
                km_arrival = int(km_arrival) if km_arrival else 0
            except ValueError:
                context['error'] = "Heure ou kilométrage invalide."
                return render(request, 'daytime/create_work.html', context)

            # Création de l'entrée
            try:
                form.create(
                    name=name,
                    hour_arrival=hour_arrival_hour,
                    km_arrival=km_arrival,
                )

                last = ChangeDaytime.objects.last()

                start.add_work(last.id, last.formel)

                return redirect('daytime')
            except Exception as e:
                error = GoogleTranslator(source='auto', target='fr').translate(str(e))
                context['error'] = f"Erreur lors de la création : {error}"
        
    
    return render(request, 'daytime/create_work.html', context)

def modify_work(request, gender, id):
    context = {
        'trucks': Truck.objects.all(),
    }
    
    if gender == 'start':
        start = StartDaytime.objects.get(id=id)
        context['title'] = 'Modification du '
        context['object'] = start
        context['user_truck'] = change_text_to_list(start.truck, '.')
        context['start'] = True
        if request.method == 'POST':
            start.truck = change_list_to_text(request.POST.getlist('truck'), '.')
            start.sector = change_list_to_text(request.POST.getlist('sector'), '.')
            start.city_start = request.POST.get('city_start').capitalize()
            start.hour_start = datetime.datetime.strptime(request.POST.get('hour_start'), '%H:%M')
            start.km_start = request.POST.get('km_start')
            start.save()
            return redirect('daytime')
        
    return render(request, 'daytime/modify_work.html', context)

def completed_work(request, gender, id):
    context = {
        'day': datetime.datetime.now(),
    }
    
    if gender == 'start':
        start = StartDaytime.objects.get(id=id)
        context['title'] = 'Terminer la journée'
        context['object'] = start
        context['gender'] = 'start'
        
        if request.method == 'POST':
            start.date_end = datetime.datetime.strptime(request.POST.get('date_end'), '%Y-%m-%d')
            start.hour_end = datetime.datetime.strptime(request.POST.get('hour_end'), '%H:%M')
            start.city_end = request.POST.get('city_end').capitalize()
            start.km_end = request.POST.get('km_end')
            start.compled = True
            start.save()
            return redirect('daytime')
    
    if gender == 'change':
        change = ChangeDaytime.objects.get(id=id)
        context['title'] = 'Terminer le changement'
        context['object'] = change
        context['gender'] = 'change'
        last_start = StartDaytime.objects.filter(name_driver=request.user.get_full_name()).last()
        
        if request.method == 'POST':
            change.hour_start = datetime.datetime.strptime(request.POST.get('hour_start'), '%H:%M')
            change.trailer = request.POST.get('trailer').upper()
            change.condition = request.POST.get('condition')
            change.lights = request.POST.get('lights')
            change.tires = request.POST.get('tires')
            change.wheight = True if int(request.POST.get('wheight')) else False
            change.comment = request.POST.get('comment')
            change.compled = True
            change.save()
            last_start.add_trailer(change.trailer)
            return redirect('daytime')
    
    return render(request, 'daytime/completed_work.html', context)
