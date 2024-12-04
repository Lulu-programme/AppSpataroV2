from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views.generic import View
from . import forms


class LoginPage(View):
    
    form_class = forms.LoginForm
    template_name = 'authentication/login.html'
    
    def get(self, request):
        form = self.form_class()
        message = ''
        context = {
            'form': form,
            'message': message,
            'title': 'Connexion'
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = self.form_class(request.POST)
        message = ''
        context = {
            'form': form,
            'message': message,
            'title': 'Connexion'
        }
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                message = 'identifiants invalides'
        return render(request, self.template_name, context)
    
    
def logout_user(request):
    logout(request)
    return redirect('login')

def profil(request):
    context = {
        'title': 'Tableau de bord'
    }
    return render(request, 'authentication/profil.html', context)
