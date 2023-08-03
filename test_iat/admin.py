from django.contrib import admin
#from .models import User, Comuna,Region,Provincia,Categoria,Cliente,Test,Caracteristica,Adjetivo,Producto,Tcategoria,Tcaracteristicas,Tadjetivos,Tproductos,Tatributos,Combinacion,Resultado
from .models.sondeo import Sondeo
from .models.descarga import Descargas
from .models.user import User 
from .models.test import Test
from .models.cliente import Cliente
from .models.comuna import Comuna
from .models.provincia import Provincia
from .models.region import Region
from .models.categoria import Categoria, Tcategoria
from .models.caracteristica import Caracteristica, Tcaracteristicas, Tatributos
from .models.adjetivo import Adjetivo, Tadjetivos
from .models.producto import Producto, Tproductos
from .models.combinacion import Combinacion
from .models.resultado import Resultado


# Register your models here.
admin.site.register(User)
admin.site.register(Comuna)
admin.site.register(Region)
admin.site.register(Provincia)
admin.site.register(Sondeo)
admin.site.register(Descargas)

admin.site.register(Categoria)

admin.site.register(Cliente)
admin.site.register(Test)
admin.site.register(Caracteristica)
admin.site.register(Adjetivo)
admin.site.register(Producto)

admin.site.register(Tcategoria)
admin.site.register(Tcaracteristicas)
admin.site.register(Tadjetivos)
admin.site.register(Tproductos)
admin.site.register(Tatributos)

admin.site.register(Combinacion)
admin.site.register(Resultado)



