from django.db import models

class Region(models.Model):
    nombre = models.CharField(max_length=100)
    ordinal = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__ (self):
        resultado={self.ordinal}+":"+ {self.nombre}
        return resultado