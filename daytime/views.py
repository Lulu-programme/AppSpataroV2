from deep_translator import GoogleTranslator
from django.shortcuts import render, redirect
from .models import StartDaytime, ChangeDaytime, FactoryDaytime, GasoilDaytime
from authentication.models import Truck
from factory.models import Factory, Station
from adr.models import Adr
from appspataroV2.tools import change_list_to_text, change_text_to_list, validate_list
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
        object = start.last()
        trailer = change_text_to_list(object.trailer, '-', '.', False)
        last_trailer = trailer[-1].upper()
        context['title'] = 'Commencer la journée'
        context['object'] = object
        context['last_trailer'] = last_trailer
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
        start_list = change_text_to_list(start.sector, ',', '.', False)
        factorys = sorted(
            [fac for fac in Factory.objects.all() if any(i in change_text_to_list(fac.sector, ',', '.', False) for i in start_list)],
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
            last_load = StartDaytime.objects.filter(name_driver=request.user.get_full_name(), last_load=True).exists()
            last_km = None

            if last_load:
                
                entry_load = StartDaytime.objects.get(name_driver=request.user.get_full_name(), last_load=True)
                same_day = entry_load.date_start == start.date_start
                
                no_filled = 0
                no_cmr = True
                nb_cmr = 0

                if same_day:  # Vérifie que c'est le même jour
                    entry = entry_load.work
                else:
                    entry = start.work
                    no_cmr = False
                    for index, work in enumerate(entry_load.work, start=1):
                        try:
                            if work.get('type') == 'factory':
                                fact = FactoryDaytime.objects.get(id=work.get('id'))
                                if fact.wheight:
                                    nb_cmr = len(change_text_to_list(fact.cmr, ',', '.', False))
                                    no_filled = index
                        except FactoryDaytime.DoesNotExist:
                            context['error'] = f"FactoryDaytime introuvable pour ID {w.get('id')}."
                    
                for w in reversed(entry):  # Parcours inverse de `work`
                    try:
                        if w.get('type') == 'factory':
                            fact = FactoryDaytime.objects.get(id=w.get('id'))
                            if fact.wheight:
                                if no_cmr:
                                    nb_cmr = len(change_text_to_list(fact.cmr, ',', '.', False))
                                if nb_cmr == no_filled:
                                    last_km = fact.km_arrival
                                else:
                                    last_km = fact.km_arrival
                                break
                            else:
                                no_filled += 1
                        elif w.get('type') == 'change':
                            change = ChangeDaytime.objects.get(id=w.get('id'))
                            last_km = change.km_arrival
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
                if last_load:
                    km_filled = km_arrival - last_km
                else:
                    km_empty = km_arrival - last_km
            else:  # Si last_km est None
                if hasattr(start, 'km_start') and start.km_start is not None:  # Vérifie si start.km_start existe
                    km_empty = km_arrival - start.km_start
                else:
                    km_empty = 0  # Valeur par défaut si aucune distance n'est définie

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
            [fac for fac in Factory.objects.all() if 'Parking' in change_text_to_list(fac.sector, ',', '.', False)],
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
        'gender': gender,
    }
    
    if gender == 'start':
        start = StartDaytime.objects.get(id=id)
        context['title'] = 'Modification du '
        context['user_truck'] = change_text_to_list(start.truck, ',', '.', False)
        context['start'] = True
        if request.method == 'POST':
            start.truck = change_list_to_text(request.POST.getlist('truck'), '.')
            start.sector = change_list_to_text(request.POST.getlist('sector'), '.')
            start.city_start = request.POST.get('city_start').capitalize()
            start.hour_start = datetime.datetime.strptime(request.POST.get('hour_start'), '%H:%M')
            start.km_start = request.POST.get('km_start')
            start.save()
            return redirect('daytime')
    
    if gender == 'factory':
        start = FactoryDaytime.objects.get(id=id)
        products = Adr.objects.all().order_by('onu')
        list_product = [prod['id'] for prod in start.get_product()]
        context['products'] = products
        context['title'] = f'Modification du travail chez {start.name}'
        
        # Retrouver la dernière remorque chargée ou vide pour récupérer le/les cmr et commande
        start_last = StartDaytime.objects.filter(name_driver=request.user.get_full_name()).order_by('-id')
        last_cmr = None
        last_command = None
        last_list_cmr = None
        last_list_command = None
        filled = None

        max_iterations = 2  # Limite à 2 éléments
        for index, entry in enumerate(start_last):
            if filled is not None or index >= max_iterations:
                break
            
            no_filled = 0
            nb_cmr = 0

            if entry.work:  # Vérifie que `work` n'est pas vide ou None
                for w in reversed(entry.work):  # Parcours inverse de `work`
                    try:
                        if w.get('type') == 'factory':
                            fact = FactoryDaytime.objects.get(id=w.get('id'))
                            if fact.wheight:
                                nb_cmr = len(change_text_to_list(fact.cmr, ',', '.', False))
                                
                                # Vérification du nombre de déchargement par rapport au nombre de cmr.
                                if nb_cmr == no_filled:
                                    break
                                elif nb_cmr > no_filled:
                                    filled = True
                                    list_product = [prod['id'] for prod in fact.get_product()]
                                    
                                    # Validation et traitement des CMR
                                    if validate_list(fact.cmr) == '1':
                                        last_cmr = fact.cmr
                                    elif validate_list(fact.cmr) == '+':
                                        last_list_cmr = change_text_to_list(fact.cmr, ',', '.', False)
                                    
                                    # Validation et traitement des commandes
                                    if validate_list(fact.command) == '1':
                                        last_command = fact.command
                                    elif validate_list(fact.command) == '+':
                                        last_list_command = change_text_to_list(fact.command, ',', '.', False)
                                    
                                    break  # Sort de la boucle dès qu'une remorque remplie est trouvée
                            else:
                                no_filled += 1
                    except FactoryDaytime.DoesNotExist:
                        context.setdefault('errors', []).append(f"FactoryDaytime introuvable pour ID {w.get('id')}.")
                    except ChangeDaytime.DoesNotExist:
                        context.setdefault('errors', []).append(f"ChangeDaytime introuvable pour ID {w.get('id')}.")
                        
        # Ajouter les résultats au contexte
        if filled:
            context['last_cmr'] = last_cmr
            context['last_command'] = last_command
            context['last_list_cmr'] = last_list_cmr
            context['last_list_command'] = last_list_command
        else:
            context['last_cmr'] = None
            context['last_command'] = None
            context['last_list_cmr'] = None
            context['last_list_command'] = None

        context['list_product'] = list_product
        
        if request.method == 'POST':
            start.start_work = datetime.datetime.strptime(request.POST.get('start_work'), '%H:%M') if request.POST.get('start_work') else None
            start.cmr = request.POST.get('cmr').upper() if request.POST.get('cmr') else None
            start.command = request.POST.get('command').upper() if request.POST.get('command') else None
            start.save()
            product = request.POST.getlist('product') if request.POST.getlist('product') else None
            
            if product:
                start.product.clear()
                for p in product:
                    detail = Adr.objects.get(id=int(p))
                    start.add_product(detail.id, detail.get_name())
            
            return redirect('daytime')
        
    context['object'] = start
    return render(request, 'daytime/modify_work.html', context)

def completed_work(request, gender, id):
    context = {
        'day': datetime.datetime.now(),
        'gender': gender,
    }
    
    if gender == 'start':
        start = StartDaytime.objects.get(id=id)
        context['title'] = 'Terminer la journée'
        context['gender'] = 'start'
        
        if request.method == 'POST':
            start.date_end = datetime.datetime.strptime(request.POST.get('date_end'), '%Y-%m-%d')
            start.hour_end = datetime.datetime.strptime(request.POST.get('hour_end'), '%H:%M')
            start.city_end = request.POST.get('city_end').capitalize()
            start.km_end = request.POST.get('km_end')
            start.compled = True
            start.save()
            return redirect('daytime')
    
    if gender == 'factory':
        start = FactoryDaytime.objects.get(id=id)
        products = Adr.objects.all().order_by('onu')
        list_product = [prod['id'] for prod in start.get_product()]
        context['products'] = products
        context['title'] = f'Terminer le travail chez {start.name}'
        
        # Retrouver la dernière remorque chargée ou vide pour récupérer le/les cmr et commande
        start_last = StartDaytime.objects.filter(name_driver=request.user.get_full_name()).order_by('-id')
        last_cmr = None
        last_command = None
        last_list_cmr = None
        last_list_command = None
        filled = None

        max_iterations = 2  # Limite à 2 éléments
        for index, entry in enumerate(start_last):
            if filled is not None or index >= max_iterations:
                break
            
            no_filled = 0
            nb_cmr = 0

            if entry.work:  # Vérifie que `work` n'est pas vide ou None
                for w in reversed(entry.work):  # Parcours inverse de `work`
                    try:
                        if w.get('type') == 'factory':
                            fact = FactoryDaytime.objects.get(id=w.get('id'))
                            if fact.wheight:
                                nb_cmr = len(change_text_to_list(fact.cmr, ',', '.', False))
                                
                                # Vérification du nombre de déchargement par rapport au nombre de cmr.
                                if nb_cmr == no_filled:
                                    break
                                elif nb_cmr > no_filled:
                                    filled = True
                                    list_product = [prod['id'] for prod in fact.get_product()]
                                    
                                    # Validation et traitement des CMR
                                    if validate_list(fact.cmr) == '1':
                                        last_cmr = fact.cmr
                                    elif validate_list(fact.cmr) == '+':
                                        last_list_cmr = change_text_to_list(fact.cmr, ',', '.', False)
                                    
                                    # Validation et traitement des commandes
                                    if validate_list(fact.command) == '1':
                                        last_command = fact.command
                                    elif validate_list(fact.command) == '+':
                                        last_list_command = change_text_to_list(fact.command, ',', '.', False)
                                    
                                    break  # Sort de la boucle dès qu'une remorque remplie est trouvée
                            else:
                                no_filled += 1
                    except FactoryDaytime.DoesNotExist:
                        context.setdefault('errors', []).append(f"FactoryDaytime introuvable pour ID {w.get('id')}.")
                    except ChangeDaytime.DoesNotExist:
                        context.setdefault('errors', []).append(f"ChangeDaytime introuvable pour ID {w.get('id')}.")
                        
        # Ajouter les résultats au contexte
        if filled:
            context['last_cmr'] = last_cmr
            context['last_command'] = last_command
            context['last_list_cmr'] = last_list_cmr
            context['last_list_command'] = last_list_command
        else:
            context['last_cmr'] = None
            context['last_command'] = None
            context['last_list_cmr'] = None
            context['last_list_command'] = None

        context['list_product'] = list_product
        if request.method == 'POST':
            start.start_work = datetime.datetime.strptime(request.POST.get('start_work'), '%H:%M') if request.POST.get('start_work') else None
            start.end_work = datetime.datetime.strptime(request.POST.get('end_work'), '%H:%M') if request.POST.get('end_work') else None
            start.hour_start = datetime.datetime.strptime(request.POST.get('hour_start'), '%H:%M') if request.POST.get('hour_start') else None
            start.cmr = request.POST.get('cmr').upper() if request.POST.get('cmr') else None
            start.command = request.POST.get('command').upper() if request.POST.get('command') else None
            start.comment = request.POST.get('comment').capitalize() if request.POST.get('comment') else None
            start.wheight = request.POST.get('wheight') if request.POST.get('wheight') else None
            start.compled = True
            start.save()
            product = request.POST.getlist('product') if request.POST.getlist('product') else None
            
            if product:
                start.product.clear()
                for p in product:
                    detail = Adr.objects.get(id=int(p))
                    start.add_product(detail.id, detail.get_name())
            
            return redirect('daytime')
    
    if gender == 'change':
        start = ChangeDaytime.objects.get(id=id)
        context['title'] = 'Terminer le changement'
        context['object'] = start
        context['gender'] = 'change'
        last_start = StartDaytime.objects.filter(name_driver=request.user.get_full_name()).last()
        
        if request.method == 'POST':
            start.hour_start = datetime.datetime.strptime(request.POST.get('hour_start'), '%H:%M')
            start.trailer = request.POST.get('trailer').upper()
            start.condition = request.POST.get('condition')
            start.lights = request.POST.get('lights')
            start.tires = request.POST.get('tires')
            start.wheight = True if int(request.POST.get('wheight')) else False
            start.comment = request.POST.get('comment')
            start.compled = True
            start.save()
            last_start.add_trailer(start.trailer)
            return redirect('daytime')
    
    context['object'] = start
    
    return render(request, 'daytime/completed_work.html', context)
