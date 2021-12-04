from ..models import Categoria
from django.core.checks import messages
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError

#CATEGORIAS
def categorias(request):
    categorias= Categoria.objects.all()
    context = {        
    "categorias":categorias,
    "accion":'default'
    }
    return render(request, 'categorias.html', context)

def categorias_new(request):
    if request.method=='GET':
        context = {        
        "accion":'new'
        }
        return render(request, 'categorias.html', context)
    if request.method == "POST":
        cat=request.POST['categoria']
        try:
            Categoria.objects.create(nombre=cat)
            messages.success(request,f'Creación de Categoria exitosa!')
        except IntegrityError:
            messages.warning(request,f'Categoria ya existe!')
        categorias= Categoria.objects.all()
        context = {        
        "categorias":categorias,
        "accion":'default'
        }
        return redirect('/categoria')

def categorias_edit(request,cat_id):
    if request.method=='GET':
        cat=Categoria.objects.get(id=cat_id)
        context = {    
            "cat":cat,    
            "accion":'edit'
        }
        return render(request, 'categorias.html', context)
    if request.method == "POST":
        cat=Categoria.objects.get(id=cat_id)
        cat.nombre=request.POST['categoria']
        cat.save()
        messages.success(request,f'Modificación de Categoria exitosa!')
        return redirect('/categoria')

def categorias_destroy(request,cat_id):
    Categoria.objects.get(id=cat_id).delete()
    messages.success(request,f'Categoria eliminada con exito!')
    return redirect('/categoria')