from django.db import models
from django.db.models.base import Model
import re

# Create your models here.

class Categoria(models.Model):
    nombre =  models.CharField(max_length=255,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Cliente(models.Model):
    nombre =  models.CharField(max_length=255,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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

class Caracteristica(models.Model):
    nombre =  models.CharField(max_length=255,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Adjetivo(models.Model):
    nombre =  models.CharField(max_length=255,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Producto(models.Model):
    nombre =  models.CharField(max_length=255,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Tcategoria(models.Model):
    categoria=models.ForeignKey(Categoria, related_name="t_cat", on_delete = models.CASCADE)
    test = models.ForeignKey(Test, related_name="categorias", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Tcaracteristicas(models.Model):
    caracteristica=models.ForeignKey(Caracteristica, related_name="t_car", on_delete = models.CASCADE)
    categoria = models.ForeignKey(Tcategoria, related_name="car_cat", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Tadjetivos(models.Model):
    adjetivo=models.ForeignKey(Adjetivo, related_name="t_adj", on_delete = models.CASCADE)
    caracteristica = models.ForeignKey(Tcaracteristicas, related_name="adj_car", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Tproductos(models.Model):
    producto =models.ForeignKey(Producto, related_name="t_prod", on_delete = models.CASCADE)
    categoria = models.ForeignKey(Tcategoria, related_name="prod_cat", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#estas seran las caracteristicas de un producto
class Tatributos(models.Model):
    caracteristica =models.ForeignKey(Caracteristica, related_name="t_atr", on_delete = models.CASCADE)
    producto = models.ForeignKey(Tproductos, related_name="prod_atr", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
            errors['password'] = "contraseña debe tener al menos 8 caracteres"

        if postData['password'] != postData['password_confirm'] :
            errors['password_confirm'] = "contraseña y confirmar contraseña no son iguales. "

        return errors

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

class Region(models.Model):
    nombre = models.CharField(max_length=100)
    ordinal = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__ (self):
        return f"{self.ordinal} : {self.nombre}"

class Provincia(models.Model):
    nombre = models.CharField(max_length=100)
    region = models.ForeignKey(Region, related_name="provincias", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__ (self):
        return f"{self.nombre}({self.id})"

class Comuna(models.Model):
    nombre = models.CharField(max_length=100)
    provincia = models.ForeignKey(Provincia, related_name="comunas", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__ (self):
        return self.nombre

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
        return f"{self.name} ({self.id})"

class Combinacion(models.Model):
    test = models.ForeignKey(Test, related_name="combinaciones", on_delete = models.CASCADE)
    participante=models.ForeignKey(User, related_name="combinaciones", on_delete = models.CASCADE)
    indice=models.IntegerField() # número de generación al iniciar el test
    analisis=models.IntegerField() # del 1 al 4
    valor=models.CharField(max_length=500)     
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
        

class Resultado(models.Model):
    milisegundos = models.FloatField()
    combinacion=models.ForeignKey(Combinacion, related_name="resultados", on_delete = models.CASCADE)
    opcion = models.CharField(max_length=2)
    pregunta = models.CharField(max_length=100)
    respuesta = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  

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
    test = models.ForeignKey(Test, related_name="sondeos", on_delete = models.CASCADE)
    participante=models.ForeignKey(User, related_name="sondeos", on_delete = models.CASCADE)
    respuesta_final= models.CharField(max_length=255, choices=RESPUESTAS,default="A")
    estado =  models.CharField(max_length=255, choices=ESTADOS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__ (self):
        return f"Test:{self.test.id} (P:{self.participante.name})[E:{self.estado}] "
    
class Descargas(models.Model):
    email=models.EmailField(max_length=255)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = DescargaManager()

    def __str__ (self):
        return f"{self.id}:{self.name} ({self.email})"