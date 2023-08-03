from django.db import models
from .user import User
from .test import Test

class Combinacion(models.Model):
    test = models.ForeignKey(Test, related_name="combinaciones", on_delete = models.CASCADE)
    participante=models.ForeignKey(User, related_name="combinaciones", on_delete = models.CASCADE)
    indice=models.IntegerField() # numero de generacion al iniciar el test
    analisis=models.IntegerField() # del 1 al 4
    valor=models.CharField(max_length=500)     
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
        