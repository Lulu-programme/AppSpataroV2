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
            load_user = StartDaytime.objects.filter(last_load=True).all() # on obtient touts les camions chargé
            unload_user = StartDaytime.objects.filter(last_load=False).all() # on obtient touts les camions déchargé
            last_user = None
            if load_user:
                if last_start.sector == 'Distribution':
                    last_user = load_user.filter(truck=last_start.truck).last() # on prend celui dont le camion correspond
                else:
                    last_user = load_user.filter(driver_name=request.user.get_full_name()).last() # on prend celui qui correspond au chauffeur
            elif unload_user:
                if last_start.sector == 'Distribution':
                    unload = unload_user.filter(truck=last_start.truck).all()
                else:
                    unload = unload_user.filter(driver_name=request.user.get_full_name()).all()
                print(f'Pas chargé : {unload}')
                for last in reversed(unload):
                    print(f'Dernier : {last}')
                    if last.work:
                        for work in reversed(last.work):
                            print(f'Travail : {work}')
                            if 'change' == work.get('type') or 'factory' == work.get('type'):
                                last_user = StartDaytime.objects.get(id=last.id)
                                break
            
            # on regarde dans le travail à quel moment il a été chargé ou déchargé
            print(f'Utilisateurs vide : {unload_user} - Utilisateurs chargé : {load_user} - utilisateur vide ou chargé : {last_user}')
            km_fill = 0
            km_empty = 0
            if last_user:
                for work in last_user.work:
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
    factorys = None
    user_truck = None
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
        user_truck = str(request.user.truck)
        
    # Contexte pour le formulaire
    context = {
        'gender': work_type,
        'title': title,
        'day': datetime.datetime.now(),
        'trucks': Truck.objects.all(),
        'last_trailer': last_trailer,
        'last_user_compled': last_user_compled if last_user_compled else None,
        'factorys': factorys,
        'user_truck': user_truck,
        # Ajouter ici les données nécessaires pour pré-remplir le formulaire
    }
    return render(request, 'daytime/create_work.html', context)


def modify_work(request, work_id):
    
    # Récupération du travail en cours et des produits à afficher
    work = FactoryDaytime.objects.get(id=work_id)
    products = Adr.objects.all().order_by('name')
    truck_loaded = StartDaytime.objects.filter(last_load=True).all() if StartDaytime.objects.filter(last_load=True).exists() else None
    last_start = StartDaytime.objects.filter(driver_name=request.user.get_full_name()).last()

    # Trouver la dernière remorque ou camion de la distribution chargé
    last_load_user = None
    if truck_loaded:
        if last_start.sector == 'Distribution':
            last_load_user = truck_loaded.filter(truck=truck_loaded.truck).last() # on prend celui dont le camion correspond
        else:
            last_load_user = truck_loaded.filter(driver_name=request.user.get_full_name()).last() # on prend celui qui le chauffeur correspond
        
    # Obtenir le(s) cmr(s) et commande(s) du chargement précédent
    load_cmr = None
    load_command = None
    load_cmr_list = None
    load_command_list = None
    load_product = None
    if last_load_user:
        for work in last_load_user.work:
            if work.get('type') == 'factory':
                factory = FactoryDaytime.objects.get(id=work.get('id'))
                if factory.weight > 0:
                    if validate_list(factory.cmr) == '+':
                        load_cmr_list = change_text_to_list(factory.cmr, ',', '.', False)
                        load_command_list = change_text_to_list(factory.command, ',', '.', False)
                        load_product = [prod['id'] for prod in factory.product]
                        break
                    else:
                        load_cmr = factory.cmr[:-1].strip()
                        load_command = factory.command[:-1].strip()
                        load_product = [prod['id'] for prod in factory.product]
                        break
            if work.get('type') == 'change':
                factory = ChangeDaytime.objects.get(id=work.get('id'))
                if factory.weight > 0:
                    if validate_list(factory.cmr) == '+':
                        load_cmr_list = change_text_to_list(factory.cmr, ',', '.', False)
                        load_command_list = change_text_to_list(factory.command, ',', '.', False)
                        load_product = [prod['id'] for prod in factory.product]
                        break
                    else:
                        load_cmr = factory.cmr[:-1].strip()
                        load_command = factory.command[:-1].strip()
                        load_product = [prod['id'] for prod in factory.product]
                        break
                    
    context = {
        'object': work,
        'products': products,
        'title': f'Modification de {work.name}',
        'last_list_cmr': load_cmr_list,
        'last_list_command': load_command_list,
        'last_cmr': load_cmr,
        'last_command': load_command,
        'list_product': load_product,
    }

    if request.method == 'POST':
        # Récupération des données
        work_start = convert_hour(request.POST.get('work_start')) if request.POST.get('work_start') else None
        cmr = request.POST.get('cmr', None)
        command = request.POST.get('command', None)
        product = request.POST.getlist('product') if request.POST.get('product') else None

        # Validation des champs
        error_cmr = '1' != validate_list(cmr) != '+' if cmr else False
        error_command = '1' != validate_list(command) != '+' if command else False

        if not error_cmr and not error_command:
            # Mise à jour des données
            work.start_work = work_start
            work.cmr = cmr
            work.command = command
            work.save()

            # Mise à jour des produits associés
            if product:
                work.product.clear()
                for p in product:
                    detail = Adr.objects.get(id=int(p))
                    work.add_product(detail.id, detail.get_name())

            return redirect('daytime')
        else:
            context.update({
                'error': f"CMR : {'il manque un point à la fin' if error_cmr else 'OK'}, "
                         f"Référence : {'il manque un point à la fin' if error_command else 'OK'}",
                'cmr': cmr,
                'command': command,
            })

    # Préparer les données pour le formulaire
    return render(request, 'daytime/modify_work.html', context)


def completed_work(request, work_type, work_id):
    
    products = Adr.objects.all().order_by('name')
    context = {
        'gender': work_type,
        'day': datetime.datetime.now(),
    }
    
    if work_type == 'change':
        change = ChangeDaytime.objects.get(id=work_id)
        start_last = StartDaytime.objects.filter(driver_name=request.user.get_full_name()).last()
        context.update({
            'title': 'Terminer un changement',
            'change': change,
            'products': products,
        })
        
        # On récupère les données du formulaire HTML
        if request.method == 'POST':
            trailer = request.POST.get('trailer').upper()
            condition = request.POST.get('condition')
            lights = request.POST.get('lights')
            tires = request.POST.get('tires')
            weight = int(request.POST.get('weight')) if request.POST.get('weight') else 0
            cmr = request.POST.get('cmr').upper() if request.POST.get('cmr') else ''
            command = request.POST.get('command').upper() if request.POST.get('command') else ''
            product = request.POST.getlist('product') if request.POST.getlist('product') else None
            hour_start = convert_hour(request.POST.get('hour_start'))
            comment = request.POST.get('comment')
            
            # Validation des champs
            error_cmr = '1' != validate_list(cmr) != '+' if cmr else False
            error_command = '1' != validate_list(command) != '+' if command else False
            
            if not error_cmr and not error_command:
                # Mise à jour des données
                change.trailer = trailer
                change.condition = condition
                change.lights = lights
                change.tires = tires
                change.weight = weight
                change.cmr = cmr
                change.command = command
                change.hour_start = hour_start
                change.comment = comment
                change.completed = True
                change.save()

                # Mise à jour des produits associés
                start_last.add_trailer(trailer)
                if weight > 0:
                    start_last.last_load = True
                if product:
                    change.product.clear()
                    for p in product:
                        detail = Adr.objects.get(id=int(p))
                        change.add_product(detail.id, detail.get_name())

                return redirect('daytime')
            else:
                context.update({
                    'error': f"CMR : {'il manque un point à la fin' if error_cmr else 'OK'}, "
                            f"Référence : {'il manque un point à la fin' if error_command else 'OK'}",
                    'cmr': cmr,
                    'command': command,
                })
    
    return render(request, 'daytime/completed_work.html', context)
