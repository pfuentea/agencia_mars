from django.core.checks import messages
from django.shortcuts import render, HttpResponse,redirect
from .models import Categoria, Cliente, Sondeo, Tcaracteristicas, Tcategoria,Test,Caracteristica,Adjetivo, Producto, Tadjetivos, User, Combinacion, Resultado
from django.contrib import messages
from django.db import IntegrityError
import random
import json
from .decorators import login_required

def get_combinaciones_elecciones2021(iat_id):
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
                if tcar.adj_car.count() > 0:
                    adj=tcar.adj_car.values_list('adjetivo_id')
                    tadj=tcar.adj_car.values_list('id')
                    #aca van las combinaciones por adjetivos 1-2, 3-4, 5-6
                    adj1=Adjetivo.objects.get(id=adj[0][0])  
                    adj2=Adjetivo.objects.get(id=adj[1][0])
                    adj3=Adjetivo.objects.get(id=adj[2][0])  
                    adj4=Adjetivo.objects.get(id=adj[3][0])
                    adj5=Adjetivo.objects.get(id=adj[4][0])  
                    adj6=Adjetivo.objects.get(id=adj[5][0])
                    # 1 con 2
                    c.append({"iat":iat.nombre,"cat":categoria.nombre,"car":c_aux.nombre,"adj1":adj1.nombre,"adj2":adj2.nombre,"tadj1":tadj[0][0],"tadj2":tadj[1][0],"adj3":adj3.nombre,"adj4":adj4.nombre,"tadj3":tadj[2][0],"tadj4":tadj[3][0],"adj5":adj5.nombre,"adj6":adj6.nombre,"tadj5":tadj[4][0],"tadj6":tadj[5][0],"pos":pos,"img1":adj1.nombre+".JPG","img2":adj2.nombre+".JPG","img3":adj3.nombre+".JPG","img4":adj4.nombre+".JPG","img5":adj5.nombre+".JPG","img6":adj6.nombre+".JPG"})
                    pos+=1
                    c.append({"iat":iat.nombre,"cat":categoria.nombre,"car":c_aux.nombre,"adj1":adj2.nombre,"adj2":adj1.nombre,"tadj1":tadj[1][0],"tadj2":tadj[0][0],"adj3":adj4.nombre,"adj4":adj3.nombre,"tadj3":tadj[3][0],"tadj4":tadj[2][0],"adj5":adj6.nombre,"adj6":adj5.nombre,"tadj5":tadj[5][0],"tadj6":tadj[4][0],"pos":pos,"img1":adj2.nombre+".JPG","img2":adj1.nombre+".JPG","img3":adj4.nombre+".JPG","img4":adj3.nombre+".JPG","img5":adj6.nombre+".JPG","img6":adj5.nombre+".JPG"})
                    pos+=1
                i+=1

    return c

def save_combinaciones(combis,test_id,user_id,analisis_id):
    test=Test.objects.get(id=test_id)
    participante=User.objects.get(id=user_id)
    index=0
    #revisamos si no existe y si no guardamos
    c_test=Combinacion.objects.filter(test=test,participante=participante)


    if c_test.count()>0:
        print("combinaciones ya existen para ese test y usuario")
    else:
        print("combinaciones no existen para ese test y usuario, se agregan")        
        for c in combis:
            #guardamos los registros            
            Combinacion.objects.create(test=test,participante=participante,indice=index,valor=c,analisis=analisis_id)
            index+=1
        print(f"Se guardaron {index} registros ")

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


#en esta parte debemos setear primero los datos que nos piden para
# perfilar al usuario antes de mostrar el START! (OK- solo falta la comuna)
@login_required
def elecciones_start(request,iat_id):
    iat=Test.objects.get(id=iat_id)
    user=User.objects.get(id=request.session['user']['id'])
    print("Elecciones_start!")
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

        if request.POST['edad'] != "":
            edad = request.POST['edad']
        else :
            messages.warning(request,f'Debe ingresar un valor valido para la edad.')  
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
        s=Sondeo.objects.create(test=iat, participante=user,estado="A")
        #print(f"sondeo_id:{s.id}")
        request.session['sondeo_id']=s.id
        #print("POR ACA PASE")
    #print(f"user:{request.session['user']['id']}")

    validaciones= get_minimo_atributos(request.session['user']['id'])
    print(f"validaciones:{validaciones}")
    if validaciones > 0:
        #Resultado.objects.all().delete()
        #Combinacion.objects.all().delete()
        request.session['iat_id']=iat_id
        request.session['analisis01']=get_combinaciones_elecciones2021(iat_id)
        save_combinaciones(request.session['analisis01'],iat_id,request.session['user']['id'],1)
        #revisamos si esta disponible el sondeo
        sondeos=Sondeo.objects.filter(test=iat, participante=user)
        if len(sondeos)>0: #que exista un sondeo
            sondeo=sondeos[0]
            request.session['sondeo_id']=sondeo.id
            print(f"Sondeo_id:{sondeo.id}")
            if sondeo.estado == "A": #en el caso que no lo finalice aun
                ok=1
            elif sondeo.estado == "R": #en el caso que lo finalice
                ok=2
        elif len(sondeos) == 0: #que no exista un sondeo
            ok=2
        
        
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
    return render(request, './elecciones2021/inicio.html', context)

#esta parte está lista
@login_required
def elecciones_test(request):
    s_id=request.session['sondeo_id']
    #print(f"S-id:{s_id}")

    if request.method == "POST":
        milisegundos=request.POST['milisegundos']
        combinacion_id=request.POST['combinacion']
        analisis=request.POST['analisis']
        opcion=request.POST['opcion']

        test=Test.objects.get(id=request.POST['iat_id'])
        user=User.objects.get(id=request.POST['user_id'])        

        print(f"pos:{combinacion_id} , analisis:{analisis},test:{request.POST['iat_id']},user:{request.POST['user_id']},opcion:{opcion}")
        combi=Combinacion.objects.filter(indice=combinacion_id,analisis=analisis,test=test,participante=user)
        llave="adj"+str(opcion)
        #print(combi.count())
        for c in combi:
            print("c:")
            print(c)
            valores=c.valor
            json_acceptable_string = valores.replace("'", "\"")
            quest = json.loads(json_acceptable_string)
            preg=quest['car']
            respuesta=quest[llave]
            #print(f"pregunta:{preg}")
            #print(f"respuesta:{respuesta}")
        #Respuesta
            res=Resultado.objects.create(combinacion=c,milisegundos=milisegundos,opcion=opcion,pregunta=preg,respuesta=respuesta)    



    if  len(request.session['analisis01']) > 0 :
        posicion_azar=random.randint(0, len(request.session['analisis01'])-1)
        combinacion=request.session['analisis01'].pop(posicion_azar)
        new_list=request.session['analisis01']
        request.session['analisis01']=new_list
    
    
        #del request.session['iat'][posicion_azar]
        #restantes
        restantes=len(request.session['analisis01'])
        #b)al enviar guardamos el resultado en la BD y quitamos esa combinacion de la lista
        context = {    
            "restantes":restantes,
            "posicion_azar":posicion_azar ,
            "combinacion":combinacion
        }
        return render(request, 'elecciones2021/test_principal.html', context)
    else:
        return redirect('/elecciones2021/end')

@login_required
def elecciones_end(request):

    #print("elecciones_end")
    if request.method == "POST":
        respuesta_final=request.POST['respuesta_final']
        print(f"R:{respuesta_final}")

        respuesta_final_save(request.session['sondeo_id'],respuesta_final)        
    
        sondeo=Sondeo.objects.get(id=request.session['sondeo_id'])
        sondeo.estado='R'
        sondeo.save()
        if 'user' in request.session:
            del request.session['user']
            return redirect('/')


        context = {    
            }
        return render(request, 'elecciones2021/final.html', context)
    else:
        context = {    
        }
        return render(request, 'elecciones2021/final.html', context)
