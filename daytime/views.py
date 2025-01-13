from django.shortcuts import render, redirect
from .models import StartDaytime, ChangeDaytime, FactoryDaytime, GasoilDaytime
from authentication.models import Truck
from factory.models import Factory, Station
from adr.models import Adr
from datacenter.models import Working, Product
from appspataroV2.tools import change_text_to_list, validate_list, change_weight, convert_date, convert_hour, hours_seconds
import datetime


def add_product_data(products, weight, date):
    data = Product.objects.get(month_year=date) if Product.objects.filter(month_year=date).exists() else None
    un_2 = ''
    weight_2 = 0
    un_3 = ''
    weight_3 = 0
    un_4 = ''
    weight_4 = 0
    un_5 = ''
    weight_5 = 0
    un_6 = ''
    weight_6 = 0
    un_8 = ''
    weight_8 = 0
    un_9 = ''
    weight_9 = 0
    
    for product in products:
        prod = Adr.objects.get(id=product.get('id'))
        if product.get('classification') == '2':
            weight_2 = change_weight(weight)
            if data and data.un_2 and str(prod.onu) in change_text_to_list(data.un_2, ',', '.', False):
                un_2 = f'{data.un_2[:-1]}, {prod.onu}.'
            else:
                un_2 = str(prod.onu)
        elif product.get('classification') == '3':
            if data and data.un_3 and str(prod.onu) in change_text_to_list(data.un_3, ',', '.', False):
                un_3 = f'{data.un_3[:-1]}, {prod.onu}.'
            else:
                un_3 = str(prod.onu)
            weight_3 = change_weight(weight)
        elif product.get('classification') == '4':
            if data and data.un_4 and str(prod.onu) in change_text_to_list(data.un_4, ',', '.', False):
                un_4 = f'{data.un_4[:-1]}, {prod.onu}.'
            else:
                un_4 = str(prod.onu)
            weight_4 = change_weight(weight)
        elif product.get('classification') == '5':
            if data and data.un_5 and str(prod.onu) in change_text_to_list(data.un_5, ',', '.', False):
                un_5 = f'{data.un_5[:-1]}, {prod.onu}.'
            else:
                un_5 = str(prod.onu)
            weight_5 = change_weight(weight)
        elif product.get('classification') == '6':
            if data and data.un_6 and str(prod.onu) in change_text_to_list(data.un_6, ',', '.', False):
                un_6 = f'{data.un_6[:-1]}, {prod.onu}.'
            else:
                un_6 = str(prod.onu)
            weight_6 = change_weight(weight)
        elif product.get('classification') == '8':
            if data and data.un_8 and str(prod.onu) in change_text_to_list(data.un_8, ',', '.', False):
                un_8 = f'{data.un_8[:-1]}, {prod.onu}.'
            else:
                un_8 = str(prod.onu)
            weight_8 = change_weight(weight)
        elif product.get('classification') == '9':
            if data and data.un_9 and str(prod.onu) in change_text_to_list(data.un_9, ',', '.', False):
                un_9 = f'{data.un_9[:-1]}, {prod.onu}.'
            else:
                un_9 = str(prod.onu)
            weight_9 = change_weight(weight)
    
    if data:
        data.un_2 = un_2 + '.' if un_2 != '' else data.un_2
        data.weight_2 += weight_2
        data.un_3 = un_3 + '.' if un_3 != '' else data.un_3
        data.weight_3 += weight_3
        data.un_4 = un_4 + '.' if un_4 != '' else data.un_4
        data.weight_4 += weight_4
        data.un_5 = un_5 + '.' if un_5 != '' else data.un_5
        data.weight_5 += weight_5
        data.un_6 = un_6 + '.' if un_6 != '' else data.un_6
        data.weight_6 += weight_6
        data.un_8 = un_8 + '.' if un_8 != '' else data.un_8
        data.weight_8 += weight_8
        data.un_9 = un_9 + '.' if un_8 != '' else data.un_8
        data.weight_9 += weight_9
        data.save()
    else:
        data = Product(
            month_year=date,
            un_2=un_2,
            weight_2=weight_2,
            un_3=un_3,
            weight_3=weight_3,
            un_4=un_4,
            weight_4=weight_4,
            un_5=un_5,
            weight_5=weight_5,
            un_6=un_6,
            weight_6=weight_6,
            un_8=un_8,
            weight_8=weight_8,
            un_9=un_9,
            weight_9=weight_9,
        )
        data.save()


def add_data_center(name, date, info, gender):
    date = datetime.datetime(date.year, date.month, 1)
    hours_day = 0
    hours_work = 0
    hours_wait = 0
    kms_total = 0
    kms_filled = 0
    kms_empty = 0
    weight = 0
    diesel = 0
    adblue = 0
    
    if gender == 'factory':
        hours_work = info.total_work(False)
        h_wait, m_wait = info.total_wait(False)
        hours_wait = hours_seconds(h_wait, m_wait)
        kms_filled = info.km_filled
        kms_empty = info.km_emptied
        weight = info.weight if info.weight > 0 else 0
        add_product_data(info.product, info.weight, date)
    elif gender == 'change':
        weight = info.weight if info.weight > 0 else 0
        add_product_data(info.product, info.weight, date)
    elif gender == 'day':
        hours_day = info.total_hours(False)
        kms_total = info.total_km()
    elif gender == 'gasoil':
        diesel = info.diesel
        adblue = info.adblue
        
    if Working.objects.filter(driver_name=name, month_year=date).exists():
        data = Working.objects.get(driver_name=name, month_year=date)
        data.hours_day += hours_day
        data.hours_work += hours_work
        data.hours_wait += hours_wait
        data.kms_total += kms_total
        data.kms_filled += kms_filled
        data.kms_empty += kms_empty
        data.weight += weight
        data.diesel += diesel
        data.adblue += adblue
        data.save()
    else:
        data = Working(
            driver_name=name,
            month_year=date,
            hours_day=hours_day,
            hours_work=hours_work,
            hours_wait=hours_wait,
            kms_total=kms_total,
            kms_filled=kms_filled,
            kms_empty=kms_empty,
            weight=weight,
            diesel=diesel,
            adblue=adblue,
        )
        data.save()


def daytime(request):
    day = datetime.date.today()
    context = {
        'title': day,
    }
    last_start = StartDaytime.objects.filter(driver_name=request.user.get_full_name()).last()
    
    if last_start:
        work_list = []
        work_end = True
        wait = None

        for work in last_start.work:
            work_type = work.get('type')
            work_id = work.get('id')
            detail = None
            if work_type == 'factory':
                detail = FactoryDaytime.objects.filter(id=work_id).first()
                wait = detail.total_wait(True) if detail.completed else None
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
            'wait': wait
        })
    
    return render(request, 'daytime/daytime.html', context)


def create_work(request, work_type):
    last_start = StartDaytime.objects.filter(driver_name=request.user.get_full_name()).last()
    last_user_completed = StartDaytime.objects.filter(driver_name=request.user.get_full_name(), completed=True).last()
    if request.method == "POST":
        # Récupération des données depuis le formulaire HTML
        if work_type == 'start':
            work_data = {
                'driver_name': request.user.get_full_name(),
                'truck': request.POST.get('truck').upper(),
                'trailer': request.POST.get('trailer', '').upper(),
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
            load_user = StartDaytime.objects.filter(last_load=True, truck=last_start.truck).all() # on obtient touts les camions chargé
            unload_user = StartDaytime.objects.filter(last_load=False, truck=last_start.truck).all() # on obtient touts les camions déchargé
            last_user = None
            if load_user: # On recherche dans les chargés
                last_user = load_user.last() # on prend celui qui correspond au chauffeur
            elif unload_user: # On recherche dans les vides
                last_user = unload_user.last()
            
            # on regarde dans le travail à quel moment il a été chargé ou déchargé
            km_fill = 0
            km_empty = 0
            if last_user:
                for work in reversed(last_user.work):
                    if work.get('type') == 'factory':
                        fact = FactoryDaytime.objects.get(id=work.get('id'))
                        if fact.weight > 0 and last_user.last_load:
                            km_fill = work_data.get('km_arrival') - fact.km_arrival
                            break
                        if fact.weight <= 0 and not last_user.last_load:
                            km_empty = work_data.get('km_arrival') - fact.km_arrival
                            break
                    if work.get('type') == 'change':
                        fact = ChangeDaytime.objects.get(id=work.get('id'))
                        if fact.weight > 0 and last_user.last_load:
                            km_fill = work_data.get('km_arrival') - fact.km_arrival
                            break
                        if fact.weight <= 0 and not last_user.last_load:
                            km_empty = work_data.get('km_arrival') - fact.km_arrival
                            break
            
            if not km_empty and not km_fill:
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
    trailer = None
    last_trailer = None
    if last_user_completed:
        if last_user_completed.sector != 'Distribution':
            if ',' in last_user_completed.trailer:
                trailer = change_text_to_list(last_user_completed.trailer, ',', '.', False)
                last_trailer = trailer[-1].upper()
            else:
                last_trailer = last_user_completed.trailer[:-1].strip()
    
    # Dénomination des titres de page
    factorys = None
    user_truck = None
    if work_type == "factory":
        title = 'Commencer un arrêt'
        factorys = sorted(
            [factory for factory in Factory.objects.all() if last_start.sector in change_text_to_list(factory.sector, ',', '.', False)],
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
        'last_user_compled': last_user_completed if last_user_completed else None,
        'factorys': factorys,
        'user_truck': user_truck,
        # Ajouter ici les données nécessaires pour pré-remplir le formulaire
    }
    return render(request, 'daytime/create_work.html', context)


def modify_work(request, work_id):
    
    # Récupération du travail en cours et des produits à afficher
    get_factory = FactoryDaytime.objects.get(id=work_id)
    products = Adr.objects.all().order_by('name')
    truck_loaded = StartDaytime.objects.filter(last_load=True).all() if StartDaytime.objects.filter(last_load=True).exists() else None
    last_start = StartDaytime.objects.filter(driver_name=request.user.get_full_name()).last()

    # Trouver la dernière remorque ou camion de la distribution chargé
    last_load_user = None
    if truck_loaded:
        if last_start.sector == 'Distribution':
            last_load_user = truck_loaded.filter(truck=last_start.truck).last() # on prend celui dont le camion correspond
        else:
            last_load_user = truck_loaded.filter(driver_name=request.user.get_full_name()).last() # on prend celui qui le chauffeur correspond
        
    # Obtenir le(s) cmr(s) et commande(s) du chargement précédent
    load_cmr = None
    load_command = None
    load_cmr_list = None
    load_command_list = None
    load_product = None
    if last_load_user:
        for work in reversed(last_load_user.work):
            if work.get('type') == 'factory':
                factory = FactoryDaytime.objects.get(id=work.get('id'))
                if factory.weight > 0:
                    if ',' in factory.cmr:
                        load_cmr_list = change_text_to_list(factory.cmr, ',', '.', False)
                        load_command_list = change_text_to_list(factory.command, ',', '.', False)
                        load_product = [prod['id'] for prod in factory.product]
                        break
                    else:
                        load_cmr = factory.cmr
                        load_command = factory.command
                        load_product = [prod['id'] for prod in factory.product]
                        break
            if work.get('type') == 'change':
                factory = ChangeDaytime.objects.get(id=work.get('id'))
                if factory.weight > 0:
                    if ',' in factory.cmr:
                        load_cmr_list = change_text_to_list(factory.cmr, ',', '.', False)
                        load_command_list = change_text_to_list(factory.command, ',', '.', False)
                        load_product = [prod['id'] for prod in factory.product]
                        break
                    else:
                        load_cmr = factory.cmr
                        load_command = factory.command
                        load_product = [prod['id'] for prod in factory.product]
                        break
    
    if get_factory.product:
        load_product = [prod['id'] for prod in get_factory.product]
                    
    context = {
        'object': get_factory,
        'products': products,
        'title': f'Modification de {get_factory.name}',
        'last_list_cmr': load_cmr_list,
        'last_list_command': load_command_list,
        'last_cmr': load_cmr,
        'last_command': load_command,
        'list_product': load_product,
    }

    if request.method == 'POST':
        # Récupération des données
        work_start = convert_hour(request.POST.get('work_start')) if request.POST.get('work_start') else None
        if load_cmr_list:
            cmr = request.POST.getlist('cmr', None)
            command = request.POST.getlist('command', None)
        else:
            cmr = request.POST.get('cmr', None)
            command = request.POST.get('command', None)
        product = request.POST.getlist('product') if request.POST.get('product') else None

        # Validation des champs
        if not load_cmr_list:
            error_cmr = '1' != validate_list(cmr) != '+' if cmr else False
            error_command = '1' != validate_list(command) != '+' if command else False
            error_product = True if len(product) > 1 and 'no' in product else False
        else:
            error_cmr, error_command, error_product = False, False, False
            cmr = f"{', '.join(c[:-1] for c in cmr)}."
            command = f"{', '.join(c[:-1] for c in command)}."

        if not error_cmr and not error_command and not error_product:
            # Mise à jour des données
            get_factory.work_start = work_start
            get_factory.cmr = cmr
            get_factory.command = command
            get_factory.save()

            # Mise à jour des produits associés
            if product:
                get_factory.product.clear()
                for p in product:
                    detail = Adr.objects.get(id=int(p))
                    get_factory.add_product(detail.id, detail.get_name(), detail.classification[0])

            return redirect('daytime')
        else:
            context.update({
                'error': f"CMR : {'il manque un point à la fin' if error_cmr else 'OK'}, "
                         f"Référence : {'il manque un point à la fin' if error_command else 'OK'}, "
                            f"Produit : {'indique qu\'il n\'y a pas de produit, alors qu\'il y en a' if error_product else 'OK' }",
                'cmr': cmr,
                'command': command,
                'work_start': work_start,
                'list_product': [int(prod) for prod in product] if not error_product else None,
            })
            
    return render(request, 'daytime/modify_work.html', context)


def completed_work(request, work_type, work_id):
    
    day = datetime.datetime.now()
    today_start = StartDaytime.objects.filter(driver_name=request.user.get_full_name()).last()
    products = Adr.objects.all().order_by('name')
    context = {
        'gender': work_type,
        'day': day,
    }
    
    if work_type == 'start':
        context.update({
            'start': today_start,
            'title': 'Terminer la journée',
        })
        
        # on récupère les données du formulaire HTML
        if request.method == 'POST':
            city_end = request.POST.get('city_end').capitalize()
            date_end = convert_date(request.POST.get('date_end'))
            hour_end = convert_hour(request.POST.get('hour_end'))
            km_end = int(request.POST.get('km_end'))
            
            # Mise à jour des données
            today_start.city_end = city_end
            today_start.date_end = date_end
            today_start.hour_end = hour_end
            today_start.km_end = km_end
            today_start.completed = True
            
            today_start.save()
            
            add_data_center(today_start.driver_name, today_start.date_start, today_start, work_type)
            
            return redirect('daytime')

    if work_type == 'gasoil':
        gasoil = GasoilDaytime.objects.get(id=work_id)
        context.update({
            'title': 'Terminer le plein',
            'gasoil': gasoil,
        })
        
        # On récupère les données du formulaire HTML
        if request.method == 'POST':
            diesel = int(request.POST.get('diesel', 0))
            adblue = int(request.POST.get('adblue', 0))
            hour_start = convert_hour(request.POST.get('hour_start'))
            
            # Mise à jour des données
            gasoil.diesel = diesel
            gasoil.adblue = adblue
            gasoil.hour_start = hour_start
            gasoil.completed = True
            gasoil.save()
            
            add_data_center(today_start.driver_name, today_start.date_start, gasoil, work_type)
            
            return redirect('daytime')
    
    if work_type == 'change':
        change = ChangeDaytime.objects.get(id=work_id)
        user_load = StartDaytime.objects.filter(driver_name=request.user.get_full_name(), last_load=True).last()
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

                # Mises à jour diverses
                today_start.add_trailer(trailer)
                # Changer les journées pour la remorque chargée
                if user_load:
                    user_load.last_load = False
                    user_load.save()
                elif weight > 0:
                    today_start.last_load = True
                    today_start.save()
                if product:
                    change.product.clear()
                    for p in product:
                        detail = Adr.objects.get(id=int(p))
                        change.add_product(detail.id, detail.get_name(), detail.classification[0])
                
                add_data_center(today_start.driver_name, today_start.date_start, change, work_type)

                return redirect('daytime')
            else:
                context.update({
                    'error': f"CMR : {'il manque un point à la fin' if error_cmr else 'OK'}, "
                            f"Référence : {'il manque un point à la fin' if error_command else 'OK'}",
                    'cmr': cmr,
                    'command': command,
                })
    
    if work_type == 'factory':
    
        # Récupération du travail en cours et des produits à afficher
        get_factory = FactoryDaytime.objects.get(id=work_id)
        products = Adr.objects.all().order_by('name')
        truck_loaded = StartDaytime.objects.filter(last_load=True).all() if StartDaytime.objects.filter(last_load=True).exists() else None

        # Trouver la dernière remorque ou camion de la distribution chargé
        last_load_user = None
        if truck_loaded:
            if today_start.sector == 'Distribution':
                last_load_user = truck_loaded.filter(truck=today_start.truck).last() # on prend celui dont le camion correspond
            else:
                last_load_user = truck_loaded.filter(driver_name=request.user.get_full_name()).last() # on prend celui qui le chauffeur correspond
            
        # Obtenir le(s) cmr(s) et commande(s) du chargement précédent et des déchargements
        load_cmr = None
        load_command = None
        load_cmr_list = None
        load_command_list = None
        load_product = None
        nb_unload = 0
        if last_load_user:
            for work in reversed(last_load_user.work):
                if work.get('type') == 'factory':
                    factory = FactoryDaytime.objects.get(id=work.get('id'))
                    if factory.weight > 0:
                        if ',' in factory.cmr:
                            load_cmr_list = change_text_to_list(factory.cmr, ',', '.', False)
                            load_command_list = change_text_to_list(factory.command, ',', '.', False)
                            load_product = [prod['id'] for prod in factory.product]
                            break
                        else:
                            load_cmr = factory.cmr
                            load_command = factory.command
                            load_product = [prod['id'] for prod in factory.product]
                            break
                    elif factory.weight <= 0:
                        nb_unload += 1
                if work.get('type') == 'change':
                    factory = ChangeDaytime.objects.get(id=work.get('id'))
                    if factory.weight > 0:
                        if ',' in factory.cmr:
                            load_cmr_list = change_text_to_list(factory.cmr, ',', '.', False)
                            load_command_list = change_text_to_list(factory.command, ',', '.', False)
                            load_product = [prod['id'] for prod in factory.product]
                            break
                        else:
                            load_cmr = factory.cmr
                            load_command = factory.command
                            load_product = [prod['id'] for prod in factory.product]
                            break
            # Vérifier si le chargement à été fait le même jour, pour avoir le nombre de déchargement
            if last_load_user.date_start != today_start.date_start:
                for work in today_start.work:
                    if work.get('type') == 'factory':
                        factory = FactoryDaytime.objects.get(id=work.get('id'))
                        if factory.weight <= 0:
                            nb_unload += 1
                
    
        if get_factory.product:
            load_product = [prod['id'] for prod in get_factory.product]
                        
        context.update({
            'factory': get_factory,
            'products': products,
            'title': f'Terminer chez {get_factory.name}',
            'last_list_cmr': load_cmr_list,
            'last_list_command': load_command_list,
            'last_cmr': load_cmr,
            'last_command': load_command,
            'list_product': load_product,
        })

        if request.method == 'POST':
            # Récupération des données
            work_start = convert_hour(request.POST.get('work_start')) if request.POST.get('work_start') else None
            end_work = convert_hour(request.POST.get('end_work')) if request.POST.get('end_work') else None
            cmr = request.POST.get('cmr', None).upper()
            command = request.POST.get('command', None).upper()
            product = request.POST.getlist('product') if request.POST.get('product') else None
            weight = int(request.POST.get('weight')) if request.POST.get('weight') else 0
            hour_start = convert_hour(request.POST.get('hour_start')) if request.POST.get('hour_start') else None
            comment = request.POST.get('comment', None).capitalize()

            # Validation des champs
            error_cmr = '1' != validate_list(cmr) != '+' if cmr else False
            error_command = '1' != validate_list(command) != '+' if command else False
            error_product = True if len(product) > 1 and 'no' in product else False

            if not error_cmr and not error_command and not error_product:
                # Mise à jour des données
                get_factory.work_start = work_start
                get_factory.end_work = end_work
                get_factory.cmr = cmr
                get_factory.command = command
                get_factory.weight = weight
                get_factory.hour_start = hour_start
                get_factory.comment = comment
                get_factory.completed = True
                get_factory.save()
                
                # Changer la journée comme jour de chargement
                if weight > 0 and not today_start.last_load: 
                    today_start.last_load = True
                    today_start.save()
                    
                # si le nombre de déchargement correspond au nombre de cmr
                elif load_cmr_list or weight <= 0:
                    if load_cmr_list:
                        if nb_unload == len(load_cmr_list): 
                            last_load_user.last_load = False
                            last_load_user.save()
                    else:
                        last_load_user.last_load = False
                        last_load_user.save()

                # Ajouter les produits dans la liste
                if 'no' not in product:
                    get_factory.product.clear()
                    for p in product:
                        detail = Adr.objects.get(id=int(p))
                        get_factory.add_product(detail.id, detail.get_name(), detail.classification[0])
            
                add_data_center(today_start.driver_name, today_start.date_start, get_factory, work_type)

                return redirect('daytime')
            else:
                context.update({
                    'error': f"CMR : {'il manque un point à la fin' if error_cmr else 'OK'}, "
                            f"Référence : {'il manque un point à la fin' if error_command else 'OK'}, "
                            f"Produit : {'indique qu\'il n\'y a pas de produit, alors qu\'il y en a' if error_product else 'OK' }",
                    'cmr': cmr,
                    'command': command,
                    'list_product': [int(prod) for prod in product] if not error_product else None,
                })
            
    return render(request, 'daytime/completed_work.html', context)
