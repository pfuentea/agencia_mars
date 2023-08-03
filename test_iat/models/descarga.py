from django.db import models
import re

class DescargaManager(models.Manager):
    def validador_basico(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        SOLO_LETRAS = re.compile(r'^[a-zA-Z. ]+$')

        errors = {}

        if len(postData['name']) < 3:
            errors['name_len'] = "Nombre debe tener al menos 3 caracteres de largo"

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "correo invalido"
            
        if not SOLO_LETRAS.match(postData['name']):
            errors['solo_letras'] = "solo letras en nombre por favor"

        return errors
    
class Descargas(models.Model):
    email=models.EmailField(max_length=255)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = DescargaManager()

    def __str__ (self):
        resultado=self.id +":"+self.name+"(" +self.email+")"
        return resultado
    
