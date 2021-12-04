from ..models import User
from django.core.checks import messages
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError


def usuarios(request):
    users=User.objects.all()
    
    context={
        "accion":"default",
        "participantes":users
        }
    return render(request, 'usuarios.html', context)

def usuarios_detalle(request,user_id):
    user=User.objects.get(id=user_id)
    context={
        "accion":"detalle",
        "Usuario":user
        }
    return render(request, 'usuarios.html', context)