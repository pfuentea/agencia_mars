from django.db import models
from .provincia import Provincia


class Comuna(models.Model):
    nombre = models.CharField(max_length=100)
    provincia = models.ForeignKey(Provincia, related_name="comunas", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__ (self):
        return self.nombre