from ..models import Cliente
from django.core.checks import messages
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError

#CLIENTE
def cliente(request):
    clientes= Cliente.objects.all()
    context = {        
    "clientes":clientes,
    "accion":'default'
    }
    return render(request, 'clientes.html', context)

def cliente_new(request):
    if request.method=='GET':
        context = {        
        "accion":'new'
        }
        return render(request, 'clientes.html', context)
    if request.method == "POST":
        cli=request.POST['cliente']
        try:
            Cliente.objects.create(nombre=cli)
            messages.success(request,f'Creación de Cliente exitosa!')
        except IntegrityError:
            messages.warning(request,f'El cliente ya existe!')
        clientes= Cliente.objects.all().order_by('-id')
        context = {        
        "clientes":clientes,
        "accion":'default'
        }
        return redirect('/cliente')

def cliente_edit(request,cli_id):
    if request.method=='GET':
        cli=Cliente.objects.get(id=cli_id)
        context = {    
            "cli":cli,    
            "accion":'edit'
        }
        return render(request, 'clientes.html', context)
    if request.method == "POST":
        cli=Cliente.objects.get(id=cli_id)
        cli.nombre=request.POST['cliente']
        cli.save()
        messages.success(request,f'Modificación de Cliente exitosa!')
        return redirect('/cliente')

def cliente_destroy(request,cli_id):
    Cliente.objects.get(id=cli_id).delete()
    messages.success(request,f'Cliente eliminado con exito!')
    return redirect('/cliente')
