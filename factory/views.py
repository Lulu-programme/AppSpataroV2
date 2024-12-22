from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Factory, Station
from appspataroV2.tools import sector_list, country_list, provision_list, language_list, reception_list, change_list_to_text, change_text_to_list, description_p
from deep_translator import GoogleTranslator
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required, user_passes_test

@login_required()
def factory_station(request):
    # Récupérer les données
    factorys_list = Factory.objects.all().order_by('name')
    stations_list = Station.objects.all().order_by('name')

    # Pagination : 10 éléments par page
    factorys_paginator = Paginator(factorys_list, 8)
    stations_paginator = Paginator(stations_list, 8)

    # Numéro des pages actuelles
    factorys_page_number = request.GET.get('page_factorys', 1)
    stations_page_number = request.GET.get('page_stations', 1)

    # Obtenir les pages actuelles
    factorys = factorys_paginator.get_page(factorys_page_number)
    stations = stations_paginator.get_page(stations_page_number)
    context = {
        'title': 'Les clients - Les stations',
        'factorys': factorys,
        'stations': stations,
    }
    return render(request, 'factory/factory_station.html', context)

@login_required()
def create_factory(request):
    context = {
        'title': 'Ajouter un client',
        'sector_list': sector_list,
        'country_list': country_list,
        'provision_list': provision_list,
        'language_list': language_list,
        'reception_list': reception_list,
    }
    if request.method == 'POST':
        try:
            # Récupération des champs du formulaire
            sector = request.POST.getlist('sector')
            name = request.POST.get('name').capitalize()
            address = request.POST.get('address').upper()
            zip_code = request.POST.get('zip_code')
            city = request.POST.get('city').capitalize()
            country = request.POST.get('country')
            gps = request.POST.get('gps')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            hourly = request.POST.get('hourly').upper()
            language = request.POST.getlist('language')
            ppe = request.POST.get('ppe')
            tools = request.POST.get('tools')
            sleep = request.POST.get('sleep')
            reception = request.POST.get('reception')
            provision = request.POST.getlist('provision')
            plan = request.FILES.get('plan')
            description = request.POST.get('description')
            
            # Conversion des listes en chaînes
            sleep_bool = True if sleep == 'Oui' else False
            sector_text = change_list_to_text(sector, '.')
            language_text = change_list_to_text(language, '.')
            provision_text = change_list_to_text(provision, '.')
            
            # Enregistrement du fichier dans le dossier media
            file_url = None
            if plan:
                fs = FileSystemStorage()
                filename = fs.save(plan.name, plan)
                file_url = fs.url(filename)
            
            # Vérification de l'usine
            inside = Factory.objects.filter(name=name, city=city).exists()
            
            if not inside:
                # Création de l'objet Factory
                Factory.objects.create(
                    sector=sector_text,
                    name=name,
                    address=address,
                    zip_code=zip_code,
                    city=city,
                    country=country,
                    gps=gps,
                    phone=phone,
                    email=email,
                    hourly=hourly,
                    language=language_text,
                    ppe=ppe,
                    tools=tools,
                    sleep=sleep_bool,
                    reception=reception,
                    provision=provision_text,
                    plan=file_url,
                    description=description,
                    slug=f'{name.lower().replace(' ', '-')}-{city.lower().replace(' ', '-')}',
                )
                return redirect('factory-station')
            else:
                factory = Factory.objects.get(name=name, city=city)
                context['error'] = f'Le client {factory.get_title()} existe déjà.'
            
        except ValueError as e:
            # Gestion des erreurs
            error = GoogleTranslator(source='auto', target='fr').translate(str(e))
            context['error'] = f"Erreur lors de l'ajout du client : {error}"
        
    return render(request, 'factory/create_factory.html', context)

@login_required()
def modify_factory(request, id):
    factory = Factory.objects.get(id=id)
    context = {
        'title': f'Modification de {factory.get_title()}',
        'sector_list': sector_list,
        'country_list': country_list,
        'provision_list': provision_list,
        'language_list': language_list,
        'reception_list': reception_list,
        'factory': factory,
        'sector_use': change_text_to_list(factory.sector, '.'),
        'language_use': change_text_to_list(factory.language, '.'),
        'provision_use': change_text_to_list(factory.provision, '.'),
    }
    if request.method == 'POST':
        try:
            # Récupération des champs du formulaire
            sector = request.POST.getlist('sector')
            name = request.POST.get('name').capitalize()
            address = request.POST.get('address').upper()
            zip_code = request.POST.get('zip_code')
            city = request.POST.get('city').capitalize()
            country = request.POST.get('country')
            gps = request.POST.get('gps')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            hourly = request.POST.get('hourly').upper()
            language = request.POST.getlist('language')
            ppe = request.POST.get('ppe')
            tools = request.POST.get('tools')
            sleep = request.POST.get('sleep')
            reception = request.POST.get('reception')
            provision = request.POST.getlist('provision')
            description = request.POST.get('description')
            
            # Conversion des listes en chaînes
            sleep_bool = True if sleep == 'Oui' else False
            sector_text = change_list_to_text(sector, '.')
            language_text = change_list_to_text(language, '.')
            provision_text = change_list_to_text(provision, '.')
            
            # Création de l'objet Factory
            factory.sector=sector_text
            factory.name=name
            factory.address=address
            factory.zip_code=zip_code
            factory.city=city
            factory.country=country
            factory.gps=gps
            factory.phone=phone
            factory.email=email
            factory.hourly=hourly
            factory.language=language_text
            factory.ppe=ppe
            factory.tools=tools
            factory.sleep=sleep_bool
            factory.reception=reception
            factory.provision=provision_text
            factory.description=description
            factory.slug=f'{name.lower().replace(' ', '-')}-{city.lower().replace(' ', '-')}'
            factory.save()
            return redirect('factory-station')
            
        except ValueError as e:
            # Gestion des erreurs
            error = GoogleTranslator(source='auto', target='fr').translate(str(e))
            context['error'] = f"Erreur lors de l'ajout du camion : {error}"
        
    return render(request, 'factory/modify_factory.html', context)

@login_required()
def create_station(request):
    context = {
        'title': 'Ajouter une station',
        'country_list': country_list,
    }
    if request.method == 'POST':
        try:
            # Récupération des champs du formulaire
            name = request.POST.get('name').upper()
            address = request.POST.get('address').upper()
            zip_code = request.POST.get('zip_code')
            city = request.POST.get('city').capitalize()
            country = request.POST.get('country')
            
            # Vérification de l'existance
            inside = Station.objects.filter(name=name, city=city)
            
            if not inside:
                # Création de l'objet Factory
                Station.objects.create(
                    name=name,
                    address=address,
                    zip_code=zip_code,
                    city=city,
                    country=country,
                )
                return redirect('factory-station')
            else:
                station = Station.objects.get(name=name, city=city)
                context['error'] = f'La station {station.get_title} existe déjà'
            
        except ValueError as e:
            # Gestion des erreurs
            error = GoogleTranslator(source='auto', target='fr').translate(str(e))
            context['error'] = f"Erreur lors de l'ajout de la station : {error}"
        
    return render(request, 'factory/create_station.html', context)

@login_required()
def modify_station(request, id):
    station = Station.objects.get(id=id)
    context = {
        'title': 'Ajouter une station',
        'country_list': country_list,
        'station': station,
    }
    if request.method == 'POST':
        try:
            # Récupération des champs du formulaire
            name = request.POST.get('name').upper()
            address = request.POST.get('address').upper()
            zip_code = request.POST.get('zip_code')
            city = request.POST.get('city').capitalize()
            country = request.POST.get('country')
            
            # Création de l'objet Factory
            station.name=name
            station.address=address
            station.zip_code=zip_code
            station.city=city
            station.country=country
            station.save()
            return redirect('factory-station')
            
        except ValueError as e:
            # Gestion des erreurs
            error = GoogleTranslator(source='auto', target='fr').translate(str(e))
            context['error'] = f"Erreur lors de l'ajout du camion : {error}"
        
    return render(request, 'factory/modify_station.html', context)

@user_passes_test(lambda user: user.is_staff)
def delete_restore(request, id, gender):
    if gender == 'factory':
        used = Factory.objects.get(id=id)
    else:
        used = Station.objects.get(id=id)
        
    if used.delete:
        used.delete = False
    else:
        used.delete = True
    used.save()
    return redirect('factory-station')

@login_required()
def detail(request, slug):
    try:
        factory = Factory.objects.get(slug=slug)
        list_description = description_p(factory.description)
        context = {
            'factory': factory,
            'descriptions': list_description,
            'title': factory.get_title(),
        }
        return render(request, 'factory/detail_factory.html', context)
    except Factory.DoesNotExist:
        return redirect('factory-station')
    