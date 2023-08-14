from django.shortcuts import render, HttpResponse,redirect


from ..models.sondeo import Sondeo
from ..models.descarga import Descargas
from ..models.user import User
from ..models.test import Test
from ..models.resultado import Resultado

def resultado(request,iat_id,analisis_id,user_id):
    iat=Test.objects.get(id=iat_id)
    participante=User.objects.get(id=user_id)
    resultados=Resultado.objects.filter(combinacion__test=iat,combinacion__participante=participante,combinacion__analisis=analisis_id)
    '''
    print(f"Resultados total:{len(resultados)}")
    valores=resultados[0].combinacion.valor
    json_acceptable_string = valores.replace("'", "\"")
    quest = json.loads(json_acceptable_string)
    print(f"quest:{quest}")
    if analisis_id == 1:
        pregunta = quest['car']
    elif analisis_id == 2:
        pregunta = quest['producto']+'-'+quest['atributo']
    '''
    #print(resultados[0].combinacion.valor)
    #print(resultados.combinacion)
    context={
        "resultados":resultados,
        "iat":iat,
        "analisis":analisis_id
        }
    return render(request, 'resultados/resultados_analisis.html', context)

def resultado_list(request,iat_id):
    iat=Test.objects.get(id=iat_id)
    
    participantes=[]
    for c in iat.combinaciones.all():
        #print(f"analisis:{c.analisis}")
        p={"nombre":c.participante.name,"user_id":c.participante.id,"analisis":c.analisis}
        participantes.append(p)

    usuarios_max_analisis = {}

    for participante in participantes:
        user_id = participante["user_id"]
        nombre = participante["nombre"]
        analisis = participante["analisis"]
        
        if user_id in usuarios_max_analisis:
            usuarios_max_analisis[user_id]["analisis"] = max(usuarios_max_analisis[user_id]["analisis"], analisis)
        else:
            usuarios_max_analisis[user_id] = {"nombre": nombre, "analisis": analisis}

    resultado = [{"user_id": user_id, "nombre": info["nombre"], "max_analisis": info["analisis"]} for user_id, info in usuarios_max_analisis.items()]
    
    for usuario in resultado:
        usuario["enlaces"] = [analisis_id for analisis_id in range(1, usuario["max_analisis"] + 1)]

    context={
        "iat":iat,
        "participantes":resultado,
        
    }
    return render(request, 'resultados/resultado.html', context)