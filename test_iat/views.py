from django.core.checks import messages
from django.shortcuts import render, HttpResponse,redirect
from .models import Categoria, Cliente,Test,Caracteristica,Adjetivo,Producto
from django.contrib import messages
from django.db import IntegrityError

def index(request):
    context = {
        'saludo': 'Hola'
    }
    return render(request, 'index.html', context)


def test(request,test_id):
    context = {
        'saludo': 'Hola'
    }
    return render(request, 'inicio.html', context)

def paso1(request):
    context = {        
    }
    return render(request, 'primera_parte.html', context)

def paso2(request):
    context = {        
    }
    return render(request, 'segunda_parte.html', context)

def paso3(request):
    context = {        
    }
    return render(request, 'tercera_parte.html', context)

def paso4(request):
    context = {        
    }
    return render(request, 'cuarta_parte.html', context)

def paso5(request):
    context = {        
    }
    return render(request, 'quinta_parte.html', context)

def final(request):
    context = {        
    }
    return render(request, 'final.html', context)


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
        Cliente.objects.create(nombre=cli)
        messages.success(request,f'Creación de Cliente exitosa!')
        clientes= Cliente.objects.all()
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
        Categoria.objects.create(nombre=cat)
        messages.success(request,f'Creación de Categoria exitosa!')
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

#PRODUCTOS
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
        Producto.objects.create(nombre=prod)
        messages.success(request,f'Creación de Producto exitosa!')
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

#CARACTERISTICAS
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
        Caracteristica.objects.create(nombre=car)
        messages.success(request,f'Creación de Caracteristica exitosa!')
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

#ADJETIVOS
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

#Creación de nuevo test:
def config_init(request):
    clientes=Cliente.objects.all()
    context={
        "clientes":clientes,
        "paso":"uno"
    }
    return render(request, 'configuracion.html', context)

#Recibo el nuevo test y le pongo una categoria:
def config_cat(request):
    testName=request.POST['testName']
    #el ciente puede ser antiguo
    cliente_id=request.POST['cliente']
    #el ciente puede ser nuevo

    categorias=Categoria.objects.all()
    context={
        "categorias":categorias,
        "paso":"dos"
    }
    return render(request, 'configuracion.html', context)