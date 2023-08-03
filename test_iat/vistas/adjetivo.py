from ..models.adjetivo import Adjetivo
from django.core.checks import messages
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError

def adjetivo(request):
    adjetivos= Adjetivo.objects.all()
    context = {        
    "adjetivos":adjetivos,
    "accion":'default'
    }
    return render(request, 'adjetivos.html', context)

def adjetivo_new(request):
    if request.method=='GET':
        context = {        
        "accion":'new'
        }
        return render(request, 'adjetivos.html', context)
    if request.method == "POST":
        adj=request.POST['adjetivo']
        try:
            Adjetivo.objects.create(nombre=adj)
            messages.success(request,f'Creación de Adjetivo exitosa!')
        except IntegrityError:
            messages.error(request,f'Este Adjetivo ya existe!')
        
        adjetivos= Adjetivo.objects.all()
        context = {        
        "adjetivos":adjetivos,
        "accion":'default'
        }
        return redirect('/adjetivo')

def adjetivo_edit(request,adj_id):
    if request.method=='GET':
        adj=Adjetivo.objects.get(id=adj_id)
        context = {    
            "adj":adj,    
            "accion":'edit'
        }
        return render(request, 'adjetivos.html', context)
    if request.method == "POST":
        adj=Adjetivo.objects.get(id=adj_id)
        adj.nombre=request.POST['adjetivo']
        try:
            adj.save()
            messages.success(request,f'Modificación de Adjetivo exitosa!')
        except IntegrityError:
            messages.error(request,f'Este Adjetivo ya existe, no se puede modificar!')
        
        return redirect('/adjetivo')

def adjetivo_destroy(request,adj_id):
    Adjetivo.objects.get(id=adj_id).delete()
    messages.success(request,f'Adjetivo eliminado con exito!')
    return redirect('/adjetivo')

