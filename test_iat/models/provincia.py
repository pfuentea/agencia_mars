from django.db import models
from .region import Region

class Provincia(models.Model):
    nombre = models.CharField(max_length=100)
    region = models.ForeignKey(Region, related_name="provincias", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__ (self):
        resultado=self.nombre+"("+self.id+")"
        return resultado