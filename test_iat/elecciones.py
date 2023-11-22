from django.core.checks import messages
from django.shortcuts import render, HttpResponse,redirect
#from .models import Categoria, Cliente, Sondeo, Tcaracteristicas, Tcategoria,Test,Caracteristica,Adjetivo, Producto, Tadjetivos, User, Combinacion, Resultado
from .models.sondeo import Sondeo
from .models.descarga import Descargas
from .models.user import User
from .models.test import Test
from .models.cliente import Cliente
from .models.categoria import Categoria, Tcategoria
from .models.caracteristica import Caracteristica, Tcaracteristicas, Tatributos
#from .models.adjetivo import Adjetivo, Tadjetivos
#from .models.producto import Producto, Tproductos
from .models.combinacion import Combinacion
from .models.resultado import Resultado
from django.contrib import messages
from django.db import IntegrityError
import random
import json
from .decorators import login_required
from .combinaciones import *

def get_combinaciones_elecciones(iat_id):
    iat=Test.objects.get(id=iat_id)
    c=[]
    if iat.categorias.count() > 0:
        tcat=Tcategoria.objects.get(id=iat.categorias.values_list('id')[0][0])
        categoria=Categoria.objects.get(id=iat.categorias.values_list('categoria_id')[0][0])
        if tcat.car_cat.count() > 0:
            car_ids=tcat.car_cat.values_list('caracteristica_id')
            tcar_ids =tcat.car_cat.values_list('id')
            i=0
            pos=0
            for r in car_ids:                
                c_aux=Caracteristica.objects.get(id=r[0])
                tcar=Tcaracteristicas.objects.get(id=tcar_ids[i][0])
                max_adj=tcar.adj_car.count()
                #print(f"ADJ_MAX:{max_adj}")
                if tcar.adj_car.count() > 0:
                    adj=tcar.adj_car.values_list('adjetivo_id')
                    tadj=tcar.adj_car.values_list('id')
                    #aca van las combinaciones por adjetivos 1-2, 3-4, 5-6
                    dict_comb={"iat":iat.nombre,"cat":categoria.nombre,"car":c_aux.nombre}
                    dict_comb_2={"iat":iat.nombre,"cat":categoria.nombre,"car":c_aux.nombre}
            
                    if max_adj == 2:
                        adj1=Adjetivo.objects.get(id=adj[0][0]) 
                        dict_comb['adj1']=adj1.nombre
                        dict_comb['tadj1']=tadj[0][0]
                        dict_comb['img1']=adj1.nombre+".JPG"
                        dict_comb['pos']=pos
                        
                        adj2=Adjetivo.objects.get(id=adj[1][0])
                        dict_comb['adj2']=adj2.nombre
                        dict_comb['tadj2']=tadj[1][0]
                        dict_comb['img2']=adj2.nombre+".JPG"
                        pos+=1      
                        dict_comb_2['adj1']=adj2.nombre
                        dict_comb_2['tadj1']=tadj[1][0]
                        dict_comb_2['img1']=adj2.nombre+".JPG"
                        
                        dict_comb_2['adj2']=adj1.nombre
                        dict_comb_2['tadj2']=tadj[0][0]
                        dict_comb_2['img2']=adj1.nombre+".JPG"
                        dict_comb_2['pos']=pos
                        pos+=1


                    if max_adj == 4:
                        adj3=Adjetivo.objects.get(id=adj[2][0])  
                        dict_comb['ajd3']=adj3.nombre
                        dict_comb['tajd3']=tadj[2][0]
                        dict_comb['img1']=adj3.nombre+".JPG"
                        adj4=Adjetivo.objects.get(id=adj[3][0])
                        dict_comb['ajd4']=adj4.nombre
                        dict_comb['tajd4']=tadj[3][0]
                        dict_comb['img2']=adj4.nombre+".JPG"
                    
                    if max_adj == 6:
                        adj5=Adjetivo.objects.get(id=adj[4][0])  
                        dict_comb['ajd5']=adj5.nombre
                        dict_comb['tajd5']=tadj[4][0]
                        dict_comb['img1']=adj5.nombre+".JPG"

                        adj6=Adjetivo.objects.get(id=adj[5][0])
                        dict_comb['ajd6']=adj6.nombre
                        dict_comb['tajd6']=tadj[5][0]
                        dict_comb['img2']=adj6.nombre+".JPG"

                    # 1 con 2
                    c.append(dict_comb)
                    
                    c.append(dict_comb_2)
                    
                i+=1

    return c
'''
def save_combinaciones(combis,test_id,user_id,analisis_id):
    print("init: save_combinaciones")
    test=Test.objects.get(id=test_id)
    participante=User.objects.get(id=user_id)
    index=0
    #revisamos si no existe y si no guardamos
    c_test=Combinacion.objects.filter(test=test,participante=participante)
    #con borra=1 elimino las combinaciones
    borrar=1
    if borrar == 1:
        c_test.delete()        
        print("se borraron las combinaciones")

    if c_test.count()>0:
        print("combinaciones ya existen para ese test y usuario")
    else:
        print("combinaciones no existen para ese test y usuario, se agregan")        
        for c in combis:
            #guardamos los registros       
            Combinacion.objects.create(test=test,participante=participante,indice=index,valor=c,analisis=analisis_id)
            index+=1
        print(f"Se guardaron {index} registros ")
    
    print("end: save_combinaciones")
'''

def get_minimo_atributos(user_id):
    u=User.objects.get(id=user_id)
    resultado=-3
    if u.edad > 0:
        resultado+=1

    if u.sexo != "N":
        resultado+=1

    if u.comuna != "":
        resultado+=1
    
    if u.ciudad != "":
        resultado+=1

    #print(f"edad:{u.edad},sexo:{u.sexo}")
    #if u.comuna != "":
    #    resultado+=1

    return resultado

def respuesta_final_save(sondeo_id,respuesta_final):
    sondeo=Sondeo.objects.get(id=sondeo_id)
    sondeo.respuesta_final= respuesta_final
    sondeo.save()

def get_faltantes(iat_id,user_id,analisis_id):
    iat=Test.objects.get(id=iat_id)
    user=User.objects.get(id=user_id)
    combi=Combinacion.objects.filter(test=iat,participante=user,analisis=analisis_id)
    faltantes=[]
    nada=0
    for c in combi:
        res=Resultado.objects.filter(combinacion=c)
        if(len(res)>0):		
            #print("Respondida!")
            nada=1
        else:
            valores=c.valor
            json_acceptable_string = valores.replace("'", "\"")
            quest = json.loads(json_acceptable_string)
            faltantes.append(quest)
    return faltantes


#en esta parte debemos setear primero los datos que nos piden para
# perfilar al usuario antes de mostrar el START! (OK- solo falta la comuna)
def elecciones2023(request):
    print("Elecciones_2023!")
    iat_id=11
    iat=Test.objects.get(id=iat_id)
    request.session['iat_nombre']=iat.nombre
    if 'init' not in request.session:
        request.session['init']='elecciones2023'
    context = {
        'invitado_nuevo':1,
        'invitado_antiguo': 0,
        'ok':0
        }
    return render(request, 'landing_estudio04.html', context)

@login_required
def elecciones_start(request,iat_id=0):
    print("Elecciones_start!")
    iat_id=11
    request.session['iat_id']=iat_id
    iat=Test.objects.get(id=iat_id)
    request.session['iat_nombre']=iat.nombre
    user=User.objects.get(id=request.session['user']['id'])
    if 'init' not in request.session:
        print("set init")
        request.session['init']='elecciones2023'

    print("Elecciones_start!")
    #print(iat.nombre)
    comuna_ok=0
    ciudad_ok=0
    comuna=""
    ciudad=""
    edad=0
    sexo="N"
    if request.method == "POST":
        if request.POST['sexo'] != "":
            sexo = request.POST['sexo']
        else :
            messages.warning(request,f'Debe seleccionar una opción de sexo.')
            sexo = 'N'

        if int(request.POST['edad']) > 0 and request.POST['edad'] != "" :
            edad = request.POST['edad']
        else :
            messages.warning(request,f'Debe ingresar una edad valida.')  
            edad = 0  
        
        comuna = request.POST['comuna'].strip()
        ciudad = request.POST['ciudad'].strip()
        #user=User.objects.get(id=request.session['user']['id'])
        if len(comuna) >0:
            comuna_ok=1
        else:
            messages.warning(request,f'Debe ingresar una comuna por favor.')  
        if len(ciudad) >0:
            ciudad_ok=1
        else:
            messages.warning(request,f'Debe ingresar una ciudad por favor.')
        user.sexo=sexo
        user.edad=edad
        user.comuna=comuna
        user.ciudad=ciudad
        user.save()
        #dejamos el sondeo activo
        s=Sondeo.objects.filter(test=iat , participante=user)
        if len(s)==0:
            print("Participante no tiene sondeo, le creamos uno")
            s=Sondeo.objects.create(test=iat, participante=user,estado="A")
            sondeo=s
        else:
            sondeo=s[0]
        print(f"sondeo_id:{sondeo.id}")
        request.session['sondeo_id']=sondeo.id
        
    #print(f"user:{request.session['user']['id']}")

    validaciones= get_minimo_atributos(request.session['user']['id'])
    print(f"validaciones:{validaciones}")
    if validaciones > 0:
        #Resultado.objects.all().delete()
        #Combinacion.objects.all().delete()
        request.session['iat_id']=iat_id
        combis=get_combinaciones_analisis01(iat_id)
        save_combinaciones(combis,iat_id,request.session['user']['id'],1)
        combis=get_combinaciones_analisis03(iat_id)
        save_combinaciones(combis,iat_id,request.session['user']['id'],3)
        #revisamos si esta disponible el sondeo
        sondeos=Sondeo.objects.filter(test=iat, participante=user)

        if len(sondeos)>0: #que exista un sondeo
            sondeo=sondeos[0]
            request.session['sondeo_id']=sondeo.id
            print(f"Sondeo_id:{sondeo.id},estado:{sondeo.estado} (A=activo,R=resuelto)")
            if sondeo.estado == "A": #en el caso que no lo finalice aun
                ok=1
            elif sondeo.estado == "R": #en el caso que lo finalice ya
                ok=2
        elif len(sondeos) == 0: #que no exista un sondeo
            s=Sondeo.objects.create(test=iat, participante=user,estado="A")
            ok=1
            
        
        
        context = {
            'saludo': 'Hola',
            "ok":ok,
            "iat_id": iat_id,
            "comuna_ok":comuna_ok,
            "ciudad_ok":ciudad_ok,
            "comuna":comuna,
            "ciudad":ciudad,
            "edad":edad,
            "sexo":sexo,
        }
        
    else:
        user=User.objects.get(id=request.session['user']['id'])
        sexo=user.sexo
        edad=user.edad
        comuna=user.comuna
        ciudad=user.ciudad
        context = {
            'saludo': 'Hola',
            "ok":0,
            "iat_id": iat_id,
            "comuna_ok":comuna_ok,
            "ciudad_ok":ciudad_ok,
            "comuna":comuna,
            "ciudad":ciudad,
            "edad":edad,
            "sexo":sexo,
        }
        print(f"IAT_ID:{iat_id}")
    return render(request, './elecciones2023/inicio.html', context)

#esta parte está lista
@login_required
def elecciones_test(request,disp):
    s_id=request.session['sondeo_id']
    iat=Test.objects.get(id=request.session['iat_id'])
    user=User.objects.get(id=request.session['user']['id'])
    #print(f"S-id:{s_id}")

    if request.method == "POST":
        # recibo la respuesta
        milisegundos=request.POST['milisegundos']
        combinacion_id=request.POST['combinacion']
        analisis=request.POST['analisis']
        opcion=request.POST['opcion']
        #obtengo el usuario y el estudio
        test=Test.objects.get(id=request.POST['iat_id'])
        user=User.objects.get(id=request.POST['user_id'])        

        print(f"pos:{combinacion_id} , analisis:{analisis},test:{request.POST['iat_id']},user:{request.POST['user_id']},opcion:{opcion}")
        #busco la combinacion
        combi=Combinacion.objects.filter(indice=combinacion_id,analisis=analisis,test=test,participante=user)
        #genero una llave con la respuesta para decir cual es el adj-n que respondió
        llave="adj"+str(opcion)
        #print(f"n_combinaciones:{combi.count()}")
        for c in combi:
            print(f"c:{c.valor}")
            valores=c.valor
            json_acceptable_string = valores.replace("'", "\"")
            quest = json.loads(json_acceptable_string)
            preg=quest['car']
            respuesta=quest[llave]
            #print(f"pregunta:{preg}")
            #print(f"respuesta:{respuesta}")
        #Respuesta
            res=Resultado.objects.create(combinacion=c,milisegundos=milisegundos,opcion=opcion,pregunta=preg,respuesta=respuesta)    

    #preguntamos si quedan preguntas(combinaciones) por responder
    #llenamos con las preguntas que faltan responder
    faltantes=[]
    faltantes=get_faltantes(iat.id,user.id,1)
    print(f"Largo analisis01:{len(faltantes)} comb")
    
    if len(faltantes) > 0 :
        posicion_azar=random.randint(0, len(faltantes)-1)
        combinacion=faltantes.pop(posicion_azar)        
        print(f"Sacamos la combinacion:{combinacion}, Tipo{type(combinacion)}")

        restantes=len(faltantes)
        #b)al enviar guardamos el resultado en la BD y quitamos esa combinacion de la lista
        context = {    
            "restantes":restantes,
            "posicion_azar":posicion_azar ,
            "combinacion":combinacion,
            "dispositivo":disp,
        }
        return render(request, 'elecciones2023/test_principal.html', context)
    else:
        print("se acabo este paso...siguiente")
        return redirect('/elecciones2023/test2/'+str(disp))


@login_required
def elecciones_test2(request,disp):
    print("T2:init")
    s_id=request.session['sondeo_id']
    iat=Test.objects.get(id=request.session['iat_id'])
    user=User.objects.get(id=request.session['user']['id'])
    #print(f"S-id:{s_id}")
    print(f"T2:RM:{request.method}")

    if request.method == "POST":
        # recibo la respuesta
        print("T2:post")
        milisegundos=request.POST['milisegundos']
        combinacion_id=request.POST['combinacion']
        analisis=3
        opcion=request.POST['opcion']
        #obtengo el usuario y el estudio
        test=Test.objects.get(id=request.POST['iat_id'])
        user=User.objects.get(id=request.POST['user_id'])        

        print(f"pos:{combinacion_id} , analisis:{analisis},test:{request.POST['iat_id']},user:{request.POST['user_id']},opcion:{opcion}")
        #busco la combinacion
        combi=Combinacion.objects.filter(indice=combinacion_id,analisis=analisis,test=test,participante=user)
        #genero una llave con la respuesta para decir cual es el adj-n que respondió
        llave="adj"+str(opcion)
        #print(f"n_combinaciones:{combi.count()}")
        for c in combi:
            print(f"c:{c.valor}")
            valores=c.valor
            json_acceptable_string = valores.replace("'", "\"")
            quest = json.loads(json_acceptable_string)
            preg=quest['car']
            respuesta=quest[llave]
            #print(f"pregunta:{preg}")
            #print(f"respuesta:{respuesta}")
        #Respuesta
            res=Resultado.objects.create(combinacion=c,milisegundos=milisegundos,opcion=opcion,pregunta=preg,respuesta=respuesta)    

    #preguntamos si quedan preguntas(combinaciones) por responder
    #llenamos con las preguntas que faltan responder
    faltantes=[]
    faltantes=get_faltantes(iat.id,user.id,3)
    print(f"Largo analisis03:{len(faltantes)}")
    
    if len(faltantes) > 0 :
        posicion_azar=random.randint(0, len(faltantes)-1)
        combinacion=faltantes.pop(posicion_azar)        
        print(f"Sacamos la combinacion:{combinacion}, Tipo{type(combinacion)}")

        restantes=len(faltantes)
        #b)al enviar guardamos el resultado en la BD y quitamos esa combinacion de la lista
        context = {    
            "restantes":restantes,
            "posicion_azar":posicion_azar ,
            "combinacion":combinacion,
            "dispositivo":disp,
        }
        return render(request, 'elecciones2023/parte_01.html', context)
    else:
        return redirect('/elecciones2023/end')

@login_required
def elecciones_end(request):
    #print("elecciones_end")
    if request.method == "POST":
        respuesta_final=request.POST['respuesta_final']
        print(f"R:{respuesta_final}")
        #guardo la respuesta de la pregunta final
        respuesta_final_save(request.session['sondeo_id'],respuesta_final)        
        #dejo el sondeo como (R)esuelto
        sondeo=Sondeo.objects.get(id=request.session['sondeo_id'])
        sondeo.estado='R'
        sondeo.save()
        #limpiamos USER para que alguien más pueda responder
        if 'user' in request.session:
            del request.session['user']
            return redirect('/elecciones2023/')

        context = {  

            }
        return render(request, 'elecciones2023/final.html', context)
    else:
        context = {    
        }
        return render(request, 'elecciones2023/final.html', context)

def regresar(request):
    if 'init' in request.session:
        estudio=request.session['init']
        
    if 'user' in request.session:
            del request.session['user']
    return redirect('/'+estudio)

#Solo pasará por aca si es un dispositivo=desktop
def instrucciones(request):
    context = {    
            }
    return render(request, 'elecciones2023/instrucciones_desktop.html', context)