from django.contrib import admin
from .models import User, Comuna,Region,Provincia,Sondeo

# Register your models here.
admin.site.register(User)
admin.site.register(Comuna)
admin.site.register(Region)
admin.site.register(Provincia)
admin.site.register(Sondeo)

