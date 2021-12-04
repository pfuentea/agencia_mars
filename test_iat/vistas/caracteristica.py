from ..models import Caracteristica
from django.core.checks import messages
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError

def caracteristica(request):
    caracteristicas= Caracteristica.objects.all()
    context = {        
    "caracteristicas":caracteristicas,
    "accion":'default'
    }
    return render(request, 'caracteristicas.html', context)

def caracteristica_new(request):
    if request.method=='GET':
        context = {        
        "accion":'new'
        }
        return render(request, 'caracteristicas.html', context)
    if request.method == "POST":
        car=request.POST['caracteristica']
        try:
            Caracteristica.objects.create(nombre=car)
            messages.success(request,f'Creación de Caracteristica exitosa!')
        except IntegrityError:
            messages.warning(request,f'Caracteristica ya existe!')
        caracteristicas= Caracteristica.objects.all()
        context = {        
        "caracteristicas":caracteristicas,
        "accion":'default'
        }
        return redirect('/caracteristica')

def caracteristica_edit(request,car_id):
    if request.method=='GET':
        car=Caracteristica.objects.get(id=car_id)
        context = {    
            "car":car,    
            "accion":'edit'
        }
        return render(request, 'caracteristicas.html', context)
    if request.method == "POST":
        Car=Caracteristica.objects.get(id=car_id)
        Car.nombre=request.POST['caracteristica']
        Car.save()
        messages.success(request,f'Modificación de Caracteristica exitosa!')
        return redirect('/caracteristica')

def caracteristica_destroy(request,car_id):
    Caracteristica.objects.get(id=car_id).delete()
    messages.success(request,f'Caracteristica eliminado con exito!')
    return redirect('/caracteristica')

