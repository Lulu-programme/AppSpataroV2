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
    if StartDaytime.objects.last():
        start = StartDaytime.objects.last()
        context['start'] = start
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
        start = StartDaytime.objects.last()
        start_list = change_text_to_list(start.sector, '.')
        factorys = sorted(
            [fac for fac in Factory.objects.all() if any(i in change_text_to_list(fac.sector, '.') for i in start_list)],
            key=lambda x: x.name  # Trie par le champ 'name' ou autre critère
        )

        form = FactoryDaytime.objects.all()
        context['factorys'] = factorys
        
        if request.method == 'POST':
            name = request.POST.get('name')
            hour_arrival = request.POST.get('hour_arrival')
            km_arrival = request.POST.get('km_arrival')
    
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
        
        if request.method == 'POST':
            start.date_end = datetime.datetime.strptime(request.POST.get('date_end'), '%Y-%m-%d')
            start.hour_end = datetime.datetime.strptime(request.POST.get('hour_end'), '%H:%M')
            start.city_end = request.POST.get('city_end').capitalize()
            start.km_end = request.POST.get('km_end')
            start.compled = True
            start.save()
            return redirect('daytime')
    
    return render(request, 'daytime/completed_work.html', context)
