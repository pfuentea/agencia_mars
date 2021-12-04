from ..models import Producto
from django.core.checks import messages
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError

def producto(request):
    productos= Producto.objects.all()
    context = {        
    "productos":productos,
    "accion":'default'
    }
    return render(request, 'productos.html', context)

def producto_new(request):
    if request.method=='GET':
        context = {        
        "accion":'new'
        }
        return render(request, 'productos.html', context)
    if request.method == "POST":
        prod=request.POST['producto']
        try:
            Producto.objects.create(nombre=prod)
            messages.success(request,f'Creación de Producto exitosa!')
        except IntegrityError:
            messages.warning(request,f'Producto ya existe!')
        productos= Producto.objects.all()
        context = {        
        "productos":productos,
        "accion":'default'
        }
        return redirect('/producto')

def producto_edit(request,prod_id):
    if request.method=='GET':
        prod=Producto.objects.get(id=prod_id)
        context = {    
            "prod":prod,    
            "accion":'edit'
        }
        return render(request, 'productos.html', context)
    if request.method == "POST":
        prod=Producto.objects.get(id=prod_id)
        prod.nombre=request.POST['producto']
        prod.save()
        messages.success(request,f'Modificación de Producto exitosa!')
        return redirect('/producto')

def producto_destroy(request,prod_id):
    Producto.objects.get(id=prod_id).delete()
    messages.success(request,f'Producto eliminado con exito!')
    return redirect('/producto')
