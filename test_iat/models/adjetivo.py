from django.db import models
from .caracteristica import Tatributos,Tcaracteristicas

class Adjetivo(models.Model):
    nombre =  models.CharField(max_length=255,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Tadjetivos(models.Model):
    adjetivo=models.ForeignKey(Adjetivo, related_name="t_adj", on_delete = models.CASCADE)
    caracteristica = models.ForeignKey(Tcaracteristicas, related_name="adj_car", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Tcalificativos(models.Model):
    calificativo=models.ForeignKey(Adjetivo, related_name="t_calif", on_delete = models.CASCADE)
    atributo = models.ForeignKey(Tatributos, related_name="calif_atrib", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)