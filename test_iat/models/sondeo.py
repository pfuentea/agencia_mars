from django.db import models
from .test import Test
from .user import User

class Sondeo(models.Model):
    ESTADOS = (
        ("A", 'Activo'),
        ("I", 'Inactivo'),
        ("R", 'Respondido'),        
    )
    RESPUESTAS =(
        ("N","No"),
        ("S","Si"),
        ("A","Sin Respuesta"),
    )
    RESPUESTA_INIT =(
        ("kast","kast"),
        ("jara","jara"),
    )
    test = models.ForeignKey(Test, related_name="sondeos", on_delete = models.CASCADE)
    participante=models.ForeignKey(User, related_name="sondeos", on_delete = models.CASCADE)
    respuesta_final= models.CharField(max_length=255, choices=RESPUESTAS,default="A")
    estado =  models.CharField(max_length=255, choices=ESTADOS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  
    respuesta_inicial= models.CharField(max_length=10, choices=RESPUESTA_INIT,default="")

    def __str__ (self):
        resultado="Test:"+str(self.test.id)+"(P:"+self.participante.name+")[E:"+self.estado+"]"
        return resultado