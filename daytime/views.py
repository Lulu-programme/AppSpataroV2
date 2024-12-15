from django.shortcuts import render, redirect
from .models import StartDaytime, ChangeDaytime, FactoryDaytime, GasoilDaytime
from authentication.models import Truck
from appspataroV2.tools import change_list_to_text
import datetime

def daytime(request):
    day = datetime.date.today()
    context = {
        'title': day,
    }
    if StartDaytime.objects.last():
        start = StartDaytime.objects.last()
        context['start'] = start
    
    return render(request, 'daytime/daytime.html', context)

def create_work(request, gender):
    context = {
        'trucks': Truck.objects.all(),
        'day': datetime.datetime.now(),
        'user_truck': str(request.user.truck)
    }
    
    if gender == 'start':
        form = StartDaytime.objects.all()
        context['title'] = 'Commencer la journée'
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
            
            form.create(
                name_driver=name_driver,
                truck=change_list_to_text(truck, '.'),
                trailer=trailer,
                sector=change_list_to_text(sector, '.'),
                city_start=city_start.capitalize(),
                date_start=date_start_date,
                hour_start=hour_start_hour,
                km_start=km_start,
            )
            return redirect('daytime')
    
    return render(request, 'daytime/create_work.html', context)
