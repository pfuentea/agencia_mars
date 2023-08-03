from django.db import models
from .categoria import Tcategoria


class Producto(models.Model):
    nombre =  models.CharField(max_length=255,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__ (self):
        return self.nombre
    

class Tproductos(models.Model):
    producto =models.ForeignKey(Producto, related_name="t_prod", on_delete = models.CASCADE)
    categoria = models.ForeignKey(Tcategoria, related_name="prod_cat", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__ (self):
        return self.producto