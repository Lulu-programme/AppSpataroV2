from django.shortcuts import render, redirect
from .models import Adr
from appspataroV2.tools import labels_list, change_list_to_text, change_text_to_list
from deep_translator import GoogleTranslator

# Create your views here.

def adr(request):
    context = {
        'title': 'Produits ADR',
        'adrs': Adr.objects.all().order_by('onu')
    }
    return render(request, 'adr/adr.html', context)

def create_product(request):
    context = {
        'title': 'Ajouter un produit',
        'labels_list': labels_list,
    }
    if request.method == 'POST':
        try:
            # Récupération des champs du formulaire
            classification = request.POST.get('classification')
            onu = request.POST.get('onu')
            name = request.POST.get('name')
            nsa = request.POST.get('nsa')
            labels = request.POST.getlist('labels')
            packing_group = request.POST.get('packing_group')
            tunnel_code = request.POST.get('tunnel_code')
            ppe = request.POST.get('ppe')
            risks = request.POST.get('risks')
            
            # Création de l'objet Factory
            Adr.objects.create(
                classification=classification,
                name=name.capitalize(),
                onu=onu,
                nsa=nsa.capitalize(),
                labels=change_list_to_text(labels, '-'),
                packing_group=packing_group,
                tunnel_code=tunnel_code.upper(),
                risks=risks.capitalize(),
                ppe=ppe.capitalize(),
            )
            return redirect('adr')
            
        except ValueError as e:
            # Gestion des erreurs
            error = GoogleTranslator(source='auto', target='fr').translate(str(e))
            context['error'] = f"Erreur lors de l'ajout du camion : {error}"
    return render(request, 'adr/create_product.html', context)

def modify_product(request, id):
    product = Adr.objects.get(id=id)
    context = {
        'title': 'Ajouter un produit',
        'labels_list': labels_list,
        'product': product,
        'list_labels': change_text_to_list(product.labels, '-')
    }
    if request.method == 'POST':
        try:
            # Récupération des champs du formulaire
            classification = request.POST.get('classification')
            onu = request.POST.get('onu')
            name = request.POST.get('name')
            nsa = request.POST.get('nsa')
            labels = request.POST.getlist('labels')
            packing_group = request.POST.get('packing_group')
            tunnel_code = request.POST.get('tunnel_code')
            ppe = request.POST.get('ppe')
            risks = request.POST.get('risks')
            
            # Création de l'objet Factory
            product.classification=classification
            product.name=name.capitalize()
            product.onu=onu
            product.nsa=nsa.capitalize()
            product.labels=change_list_to_text(labels, '-')
            product.packing_group=packing_group
            product.tunnel_code=tunnel_code.upper()
            product.risks=risks.capitalize()
            product.ppe=ppe.capitalize()
            product.save()
            return redirect('adr')
            
        except ValueError as e:
            # Gestion des erreurs
            error = GoogleTranslator(source='auto', target='fr').translate(str(e))
            context['error'] = f"Erreur lors de l'ajout du camion : {error}"
    return render(request, 'adr/modify_product.html', context)

def delete_restore(request, id):
    product = Adr.objects.get(id=id)
    if product.delete:
        product.delete = False
    else:
        product.delete = True
    product.save()
    return redirect('adr')
