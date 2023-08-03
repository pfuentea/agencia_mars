from django.db import models
from .test import Test 

class Categoria(models.Model):
    nombre =  models.CharField(max_length=255,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Tcategoria(models.Model):
    categoria=models.ForeignKey(Categoria, related_name="t_cat", on_delete = models.CASCADE)
    test = models.ForeignKey(Test, related_name="categorias", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)