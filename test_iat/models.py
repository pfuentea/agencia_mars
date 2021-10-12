from django.db import models


# Create your models here.

class Categoria(models.Model):
    nombre =  models.CharField(max_length=255,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Cliente(models.Model):
    nombre =  models.CharField(max_length=255,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Test(models.Model):
    nombre = models.CharField(max_length=255)
    cliente = models.ForeignKey(Cliente, related_name="tests", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Caracteristica(models.Model):
    nombre =  models.CharField(max_length=255,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Adjetivo(models.Model):
    nombre =  models.CharField(max_length=255,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Producto(models.Model):
    nombre =  models.CharField(max_length=255,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Tcategoria(models.Model):
    categoria=models.ForeignKey(Categoria, related_name="t_cat", on_delete = models.CASCADE)
    test = models.ForeignKey(Test, related_name="categorias", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Tcaracteristicas(models.Model):
    caracteristica=models.ForeignKey(Caracteristica, related_name="t_car", on_delete = models.CASCADE)
    categoria = models.ForeignKey(Tcategoria, related_name="car_cat", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Tadjetivos(models.Model):
    adjetivo=models.ForeignKey(Adjetivo, related_name="t_adj", on_delete = models.CASCADE)
    caracteristica = models.ForeignKey(Tcaracteristicas, related_name="adj_car", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Tproductos(models.Model):
    producto =models.ForeignKey(Producto, related_name="t_prod", on_delete = models.CASCADE)
    categoria = models.ForeignKey(Tcategoria, related_name="prod_cat", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)