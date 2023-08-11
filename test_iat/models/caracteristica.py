from django.db import models
from .categoria import Tcategoria

class Caracteristica(models.Model):
    nombre =  models.CharField(max_length=255,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Tcaracteristicas(models.Model):
    caracteristica=models.ForeignKey(Caracteristica, related_name="t_car", on_delete = models.CASCADE)
    categoria = models.ForeignKey(Tcategoria, related_name="car_cat", on_delete = models.CASCADE)
    analisis = models.IntegerField() # del 1 al 4
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__ (self):
        resultado=self.caracteristica.nombre+"("+str(self.id)+"/("+str(self.analisis)+"))"
        return resultado

class Tatributos(models.Model):
    caracteristica =models.ForeignKey(Caracteristica, related_name="t_atr", on_delete = models.CASCADE)
    categoria = models.ForeignKey(Tcategoria, related_name="atr_cat", on_delete = models.CASCADE)
    analisis = models.IntegerField(default=2) # del 1 al 4
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__ (self):
        resultado=self.caracteristica.nombre+"("+str(self.id)+")"
        return resultado