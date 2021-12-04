from ..models import Sondeo,User,Test
from django.core.checks import messages
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError

def sondeos(request):
    if request.method=='POST':
        test = Test.objects.get(id=request.POST['iat'])
        user =  User.objects.get(id=request.POST['user'])
        s=Sondeo.objects.filter(test=test,participante=user)
        print(f"t:{request.POST['iat']},u:{request.POST['user']}")
        if len(s) == 0 :
            sond= Sondeo.objects.create(test=test,participante=user,estado="A")
            print("nuevo")
        else:
            print("existe")
            result= s.values_list('id')
            sond=Sondeo.objects.get(id=result[0][0])
            sond.estado="A"
            sond.save()

    iats= Test.objects.all()
    participantes=User.objects.all()
    sondeos_activos=Sondeo.objects.all()
    context={
        "accion":"default",
        "iats":iats,
        "participantes":participantes,
        "sondeos":sondeos_activos
        }
    return render(request, 'sondeos.html', context)

def sondeos_deactivate(request,s_id):
    sondeo=Sondeo.objects.get(id=s_id)
    sondeo.estado='I'
    sondeo.save()
    return redirect('/sondeos')

def sondeos_destroy(request,s_id):
    sondeo=Sondeo.objects.get(id=s_id).delete()
    
    return redirect('/sondeos')