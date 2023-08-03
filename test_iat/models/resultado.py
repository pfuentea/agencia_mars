from django.db import models
from .combinacion import Combinacion


class Resultado(models.Model):
    milisegundos = models.FloatField()
    combinacion=models.ForeignKey(Combinacion, related_name="resultados", on_delete = models.CASCADE)
    opcion = models.CharField(max_length=2)
    pregunta = models.CharField(max_length=100)
    respuesta = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  