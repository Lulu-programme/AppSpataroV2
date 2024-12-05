from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Truck, Account
from datetime import datetime


@login_required
def profil(request):
    context = {
        'title': 'Tableau de bord'
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
            context['error'] = f"Erreur lors de l'ajout du camion : {e}"
    
    return render(request, 'authentication/truck.html', context)

def signup_page(request):
    pass
