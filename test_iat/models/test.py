from django.db import models
from .cliente import Cliente

class Test(models.Model):
    TYPES = (
        ("normal", 'Normal'),
        ("elecciones2021", 'Elecciones 2021')
    )
    nombre = models.CharField(max_length=255)
    cliente = models.ForeignKey(Cliente, related_name="tests", on_delete = models.CASCADE)
    tipo =models.CharField(max_length=255,default="normal")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('-created_at',)

    def __str__ (self):
        return self.nombre