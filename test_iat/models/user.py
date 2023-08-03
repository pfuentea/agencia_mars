from django.db import models
import re

class UserManager(models.Manager):
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

        if len(postData['password']) < 8:
            errors['password'] = "el password debe tener al menos 8 caracteres"

        if postData['password'] != postData['password_confirm'] :
            errors['password_confirm'] = "password y confirmar password no son iguales. "

        return errors
    

class User(models.Model):
    CHOICES = (
        ("user", 'User'),
        ("mars", 'MARS'),
        ("guest", 'Invitado'),
        ("admin", 'Admin')
    )
    SEXO = (
        ("M", 'Masculino'),
        ("F", 'Femenino'),
        ("O","Otro"),
        ("N","Ninguno")
    )
    email=models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=255, choices=CHOICES)
    password = models.CharField(max_length=70)
    edad= models.IntegerField(default=0)
    sexo =  models.CharField(max_length=2, choices=SEXO, default="N")
    #comuna = models.ForeignKey(Comuna, related_name="pobladores", on_delete = models.CASCADE, default='' )
    comuna =  models.CharField(max_length=70,default="")
    ciudad =  models.CharField(max_length=70,default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    
    def __str__ (self):
        resultado=self.name+"("+str(self.id)+")"
        return resultado