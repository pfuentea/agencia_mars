from django.core.checks import messages
from django.shortcuts import render, HttpResponse,redirect
#from .models import Categoria, Cliente, Descargas, Tcaracteristicas, Tcategoria,Test,Caracteristica,Adjetivo, Producto, Tadjetivos, User, Combinacion, Resultado, Sondeo
#from .models import Categoria, Cliente, Descargas, Tcaracteristicas, Tcategoria,Test,Caracteristica,Adjetivo, Producto, Tadjetivos, User, Combinacion, Resultado, Sondeo

from .models.sondeo import Sondeo
from .models.descarga import Descargas
from .models.user import User
from .models.test import Test
#from .models.cliente import Cliente
#from .models.comuna import Comuna
#from .models.provincia import Provincia
#from .models.region import Region
#from .models.categoria import Categoria, Tcategoria
#from .models.caracteristica import Caracteristica, Tcaracteristicas, Tatributos
#from .models.adjetivo import Adjetivo, Tadjetivos
#from .models.producto import Producto, Tproductos
#from .models.combinacion import Combinacion
from .models.resultado import Resultado

from django.contrib import messages
from django.db import IntegrityError
from django.template import Context, loader

import json
from .decorators import login_required 

from .forms.emailForm import EmailForm
def clean(request):
    print("limpando variable init")
    if 'init' in request.session:
        del request.session['init']
    print("limpando variable iat_id")
    if 'iat_id' in request.session:
        del request.session['iat_id']
    return redirect( '/' )

def landing(request):
    print("Landing")
    emailForm=EmailForm()
    context = {
        "emailForm":emailForm
    }
    if 'init' in request.session:
        print("init:ELECCIONES 2023")
        context = {
            'invitado_nuevo':1,
            'invitado_antiguo': 0,
        }
        return render(request, 'elecciones2023/inicio.html', context)
    #print(f"VIEW-L:ref:{ref}")
    return render(request, 'landing.html', context)

def sitio_privado(request):
    
    user=User.objects.get(id=request.session['user_id'])
    estudios=Sondeo.objects.filter(participante=user,estado='A')

    print(f"Estudios:{estudios.count()}")
    for e in estudios:
        print(e)

    context = {
        "estudios":estudios
    }
    return render(request, 'sitio_privado.html', context)

def index_resultados(request):
    context = {
        "saludo":"hola"
    }
    return render(request, 'index_resultados.html', context)

def descarga_resultados(request):
    if request.method == "POST":
        email=request.POST['email']
        nombre=request.POST['nombre']
        descarga= Descargas.objects.create(email=email,name=nombre)
        context = {
            "nombre":nombre
        }
        return render(request, 'descarga.html', context)

    if request.method == "GET":
        return redirect('')

def index(request):

    invitado_antiguo=0
    # aca seteamos el id que dejamos disponible
    if request.session['iat_id'] :
            estudio_id=request.session['iat_id']
    else:
        estudio_id=10
        
    
    #entro al index, existe la variable USER(ingreso al index antes), pero no FROM_LOGIN(usuario tipo user y no guest) => limpiamos USER
    if request.method == "GET":
        if 'user' in request.session and 'from_login' not in request.session :
            del request.session['user']
            print("delete session-user")

    # ingreso al index desde el formulario de nombre-email
    if request.method == "POST":
        nombre=request.POST['nombre']
        email=request.POST['email']

        if nombre =="":
            nombre="Invitado"
        #intentamos crear un usuario invitado,FAIL=> ya existe    
        try:
            new_user=User.objects.create(email=email,name=nombre,role='guest')
            user = {
                    "id" : new_user.id,
                    "name": f"{new_user.name}",
                    "email": new_user.email,
                    "role": new_user.role,
                }
            request.session['user'] = user
        except IntegrityError:
            invitado_antiguo=1
            result=User.objects.filter(email=email)
            new_user=result[0]
            #print(f"EMAIL:{new_user.email}")
            user = {
                    "id" : new_user.id,
                    "name": f"{new_user.name}",
                    "email": new_user.email,
                    "role": new_user.role,
                }
            request.session['user'] = user
        #comenzamos asumiento que invitado_antiguo=0 (falso)    
        #en este punto hay dos posibilidades usuario-nuevo=>user, usuario_antiguo=>user
    #print("INDEX")


    #esto lo hacemos para verificar si ya habia entrado y cerro la página o viene de otro lado (escribio la url de nuevo )
    user_nuevo=1
    if "user" not in request.session:
        print("INVITADO NUEVO!")
        #le pedimos su Correo, a menos que sea antiguo, en ese caso no
    else:
        #usuario=User.objects.get(id=request.session['user']['id'])
        print("INVITADO ANTIGUO!")
        user_nuevo=0
    
    #revisamos si puede hacer el sondeo
    if invitado_antiguo == 1:
        iat=Test.objects.get(id=iat_id)
        print(f"participante:{new_user.name}")
        s=Sondeo.objects.filter(test=iat , participante=new_user)
        if len(s)==0:
            invitado_antiguo=0
            user_nuevo=0
            print("NO TIENE SONDEO!")
            s=Sondeo.objects.create(test=iat , participante=new_user,estado="A")
            print("Sondeo creado.")
        else:
            print(f"TIENE SONDEO!({len(s)})")
            print(f"sondeo detectado:{s[0].id}")
            invitado_antiguo=0

    #print("viene el ctx!")
    context = {
        'invitado_nuevo':user_nuevo,
        'invitado_antiguo': invitado_antiguo,
    }
    #Combinacion.objects.all().delete()
    #Resultado.objects.all().delete()
    #print("viene el render!")
    if user_nuevo == 0 and invitado_antiguo == 0:
        return redirect('/estudio/start/'+str(iat_id))  #esa ruta debe ser variable segun test activo
    else:
        return render(request, 'landing_estudio04.html', context) #esa ruta debe ser variable segun test activo

def login(request):
    context = {
        'saludo': 'Hola'
    }
    return render(request, 'login.html', context)

def registro(request):
    context = {
        'saludo': 'Hola'
    }
    return render(request, 'registro.html', context)
    

## MANTENEDORES
#CLIENTE
# en vistas/cliente.py

#CATEGORIAS
# en vistas/categoria.py

#PRODUCTOS
# en vistas/producto.py

#CARACTERISTICAS
# en vistas/caracteristica.py

#ADJETIVOS
# en vistas/adjetivo.py

#Creación de nuevo test:

#RESULTADOS
# en vistas/resultado.py

#USUARIOS
# en vistas/usuarios.py
