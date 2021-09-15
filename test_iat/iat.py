from .models import *

def analisis_categoria(categoria_id,caracteristicas,adjetivos):
    #con una categoria, algunas caracteristicas, algunos adjetivos
    pasos=[]
    cat=Categoria.objects.get(id=categoria_id)


