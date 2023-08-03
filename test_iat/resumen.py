#from .models import Caracteristica, Test, User,Tcategoria,Categoria,Tcaracteristicas,Adjetivo

#from .models.sondeo import Sondeo
#from .models.descarga import Descargas
from .models.user import User
from .models.test import Test
#from .models.cliente import Cliente
#from .models.comuna import Comuna
#from .models.provincia import Provincia
#from .models.region import Region
from .models.categoria import Categoria, Tcategoria
from .models.caracteristica import Caracteristica, Tcaracteristicas, Tatributos
from .models.adjetivo import Adjetivo, Tadjetivos
#from .models.producto import Producto, Tproductos
#from .models.combinacion import Combinacion
from .models.resultado import Resultado
from django.core.checks import messages
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError

def resumen(request,iat_id):
    iat=Test.objects.get(id=iat_id)
    caracteristicas= iat.categorias.all()
    tcat=Tcategoria.objects.get(id=iat.categorias.values_list('id')[0][0])
    categoria=Categoria.objects.get(id=iat.categorias.values_list('categoria_id')[0][0])
    preguntas=[]  
    print (f"CAT:{categoria.nombre}")

    car_ids=tcat.car_cat.values_list('caracteristica_id')
    tcar_ids =tcat.car_cat.values_list('id')
    i=0
    for cr in car_ids:
        c_aux=Caracteristica.objects.get(id=cr[0])
        tcar=Tcaracteristicas.objects.get(id=tcar_ids[i][0])
        print(f"caux:{c_aux.nombre}")
        preguntas.append(c_aux.nombre)
        adj=tcar.adj_car.values_list('adjetivo_id')
        tadj=tcar.adj_car.values_list('id')
        adj1=Adjetivo.objects.get(id=adj[0][0])
        print(f"ADJ:{adj1.nombre}")

    context={
        "accion":"default",
        "iat":iat,
        "preguntas":preguntas,
        }
    return render(request, 'resumen.html', context)