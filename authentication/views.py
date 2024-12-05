from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Truck, Account
from datetime import datetime
from deep_translator import GoogleTranslator


@login_required
def profil(request):
    context = {
        'title': 'Tableau de bord',
        'trucks': Truck.objects.all(),
        'drivers': Account.objects.all(),
    }
    return render(request, 'authentication/profil.html', context)

def login_page(request):
    context = {
        'title': 'Connexion'
    }
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user is not None:
            login(request, user)
            return redirect('profil')
        else:
            context['message'] = f'{request.POST['username']} invalide.'
    return render(request, 'authentication/login.html', context)
    
def logout_user(request):
    logout(request)
    return redirect('login')

def add_truck(request):
    context = {
        'title': 'Ajouter un camion'
    }
    if request.method == 'POST':
        try:
            license = request.POST.get('license', '').upper()
            technical = request.POST.get('technical')
            tachographe = request.POST.get('tachographe')
            maintenance = request.POST.get('maintenance')
            adr = request.POST.get('adr')
            weight = request.POST.get('weight')

            # Conversion des dates
            technical_date = datetime.strptime(technical, '%Y-%m-%d') if technical else None
            tachographe_date = datetime.strptime(tachographe, '%Y-%m-%d') if tachographe else None
            maintenance_date = datetime.strptime(maintenance, '%Y-%m-%d') if maintenance else None
            adr_date = datetime.strptime(adr, '%Y-%m-%d') if adr else None

            # Création du camion
            Truck.objects.create(
                license=license,
                technical=technical_date,
                tachographe=tachographe_date,
                maintenance=maintenance_date,
                adr=adr_date,
                weight=weight,
            )
            return redirect('profil')
        except ValueError as e:
            # Gestion des erreurs de conversion
            error = GoogleTranslator(source='auto', target='fr').translate(str(e))
            context['error'] = f"Erreur lors de l'ajout du camion : {error}"
    
    return render(request, 'authentication/truck.html', context)

def signup_page(request):
    context = {
        'title': 'Ajouter un chauffeur',
        'trucks': Truck.objects.all(),
    }
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                username = request.POST.get('username')
                password = request.POST.get('password1')
                first_name = request.POST.get('first_name').capitalize()
                last_name = request.POST.get('last_name').capitalize()
                sector = request.POST.get('sector')
                truck = request.POST.get('truck')
                drive_license = request.POST.get('drive_license')
                adr_license = request.POST.get('adr_license')
                card_drive = request.POST.get('card_drive')
                email = request.POST.get('email')
                phone = request.POST.get('phone')
                city = request.POST.get('city').capitalize()
                is_staff = request.POST.get('is_staff')

                # Conversion des dates
                drive_license_date = datetime.strptime(drive_license, '%Y-%m-%d') if drive_license else None
                adr_license_date = datetime.strptime(adr_license, '%Y-%m-%d') if adr_license else None
                card_drive_date = datetime.strptime(card_drive, '%Y-%m-%d') if card_drive else None

                # Création du camion
                Account.objects.create_user(
                    username=username,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    sector=sector,
                    truck=Truck.objects.get(id=truck) if truck else None,
                    drive_license=drive_license_date,
                    adr_license=adr_license_date,
                    card_drive=card_drive_date,
                    email=email,
                    phone=phone,
                    city=city,
                    is_staff=True if is_staff else False,
                )
                return redirect('profil')
            except ValueError as e:
                # Gestion des erreurs de conversion
                error = GoogleTranslator(source='auto', target='fr').translate(str(e))
                context['error'] = f"Erreur lors de l'ajout du chauffeur : {error}"
        else:
            context['error'] = 'les mots de passe ne correspondent pas'
    
    return render(request, 'authentication/signup.html', context)
