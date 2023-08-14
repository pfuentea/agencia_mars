#from ..models import Test,Cliente,Categoria,Tcategoria,Caracteristica,Tcaracteristicas,Adjetivo,Tadjetivos,User,Combinacion,Resultado, Sondeo, Producto,Tproductos, Tatributos,Tcalificativos
from ..models.sondeo import Sondeo
from ..models.descarga import Descargas
from ..models.user import User
from ..models.test import Test
from ..models.cliente import Cliente
#from ..models.comuna import Comuna
#from ..models.provincia import Provincia
#from ..models.region import Region
from ..models.categoria import Categoria, Tcategoria
from ..models.caracteristica import Caracteristica, Tcaracteristicas, Tatributos
from ..models.adjetivo import Adjetivo, Tadjetivos, Tcalificativos
from ..models.producto import Producto, Tproductos
from ..models.combinacion import Combinacion
from ..models.resultado import Resultado

from django.core.checks import messages
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError
from ..combinaciones import get_combinaciones_analisis01,get_combinaciones_analisis02,get_combinaciones_analisis03,get_combinaciones_analisis04,save_combinaciones
import random


def iat(request):
    iats=Test.objects.all()

    context={
        "iats":iats,
        "accion":'default'
    }
    return render(request, 'iat.html', context)

def exec_test(request):

    pass

def config(request,iat_id):
    context = {        
        "iat_id":iat_id
        }
    return render(request, 'config_iat.html', context)

def config_pms(request,iat_id): #analisis02
    iat=Test.objects.get(id=iat_id)
    productos=[]
    atributos=[]
    combinaciones=[]
    participantes=[]
    print(f"Cantidad de categorias:{iat.categorias.count()}")
    if iat.categorias.count() > 0: # si existe categoria podrían existir productos
        tcat=Tcategoria.objects.get(id=iat.categorias.values_list('id')[0][0])
        categoria=Categoria.objects.get(id=iat.categorias.values_list('categoria_id')[0][0])
        #productos de la categoria
        result_prod_id=tcat.prod_cat.values_list('producto_id')
        result_tprod_id =tcat.prod_cat.values_list('id')
        i=0
        for r in result_prod_id:
            p_aux=Producto.objects.get(id=r[0])
            #tprod=Tproductos.objects.get(id=result_tprod_id[i][0])
            productos.append({"id": result_tprod_id[i][0],"nombre":p_aux.nombre})
            i+=1
        #atributos de la categoria (que deben cruzarse con los productos)
        print(f"Cantidad de atributos:{tcat.atr_cat.count()}")
        '''
        atr_instance = Tcaracteristicas.objects.first()
        attributes_and_methods = dir(atr_instance)
        for attribute_or_method in attributes_and_methods:
            print(attribute_or_method)
        '''

        result_atr_id=tcat.atr_cat.values_list('caracteristica_id')
        result_tatr_id =tcat.atr_cat.values_list('id')
        j=0
        for r in result_atr_id:
            print(f"R:{r}-{result_tatr_id[j][0]}")
            at_aux=Caracteristica.objects.get(id=r[0])
            tatrib=Tatributos.objects.get(id=result_tatr_id[j][0])
            n_calif=tatrib.calif_atrib.count()
            atributos.append({"id": result_tatr_id[j][0],"nombre":at_aux.nombre,"n_calif":n_calif})
            
            j+=1

    prods=Producto.objects.all()
    atribs=Caracteristica.objects.all()
    combinaciones=get_combinaciones_analisis02(iat_id)
    for c in iat.combinaciones.all():
            p={"nombre":c.participante.name,"user_id":c.participante.id}
            participantes.append(p)

    participantes=[dict(t) for t in {tuple(d.items()) for d in participantes}]
        
    #print(f"Cantidad de prods:{prods.count()}") #producto para el selector
    context = {        
        "iat_id":iat_id,
        "iat":iat,
        "categoria":categoria,
        "tcat":tcat,
        "productos":productos,
        "prods":prods,
        "atributos":atributos,
        "atribs":atribs,
        "combinaciones":combinaciones,
        "participantes":participantes
        }
    return render(request, 'config_analisis02.html', context)

def iat_add_prod(request,iat_id):
    #falta validar que no se agregue 2 veces
    iat=Test.objects.get(id=iat_id)
    tcat=Tcategoria.objects.get(id=iat.categorias.values_list('id')[0][0])
    if request.POST['prod'] =='':
        messages.warning(request,f'Seleccione una opcion!')    
        return redirect('/config_02/'+str(iat_id))
    if request.POST['prod'] =='otro':
        print(request.POST['new_prod'])
        if request.POST['new_prod'] == "":
            messages.warning(request,'El producto no puede ser vacío')
            return redirect('/config_02/'+str(iat_id))
        else:    
            try:
                producto= Producto.objects.create(nombre=request.POST['new_prod'])
                messages.success(request,f'Producto creado exitosamente!')
            except IntegrityError:
                messages.error(request,f'Este producto ya existe!')
                producto=Producto.objects.get(nombre=request.POST['new_prod'])         
    else:
        producto=Producto.objects.get(id=request.POST['prod']) 
    #agregamos el  producto a la categoria
    # tcat.prod_cat.nombre
    #new_car=Tcaracteristicas.objects.create(caracteristica=caract,categoria=tcat)
    new_prod=Tproductos.objects.create(producto=producto,categoria=tcat)
    messages.success(request,f'Producto agregado exitosamente!')
    
    return redirect('/config_02/'+str(iat_id))

def iat_add_atrib(request,iat_id):
    #falta validar que no se agregue 2 veces
    iat=Test.objects.get(id=iat_id)
    tcat=Tcategoria.objects.get(id=iat.categorias.values_list('id')[0][0])
    if request.POST['atrib'] =='':
        messages.warning(request,f'Seleccione una opcion!')    
        return redirect('/config_02/'+str(iat_id))
    if request.POST['atrib'] =='otro':
        print(request.POST['new_atrib'])
        if request.POST['new_atrib'] == "":
            messages.warning(request,'El atributo no puede ser vacío')
            return redirect('/config_02/'+str(iat_id))
        else:    
            try:
                atributo= Caracteristica.objects.create(nombre=request.POST['new_atrib'])
                messages.success(request,f'Atributo creado exitosamente!')
            except IntegrityError:
                messages.error(request,f'Este atributo ya existe!')
                atributo=Caracteristica.objects.get(nombre=request.POST['new_atrib'])         
    else:
        atributo=Caracteristica.objects.get(id=request.POST['atrib']) 
    #agregamos el  producto a la categoria
    # tcat.prod_cat.nombre
    #new_car=Tcaracteristicas.objects.create(caracteristica=caract,categoria=tcat)
    new_atr=Tatributos.objects.create(caracteristica=atributo,categoria=tcat)
    messages.success(request,f'Atributo agregado exitosamente!')
    
    return redirect('/config_02/'+str(iat_id))

def iat_rem_prod(request,iat_id):
    pass

def iat_rem_atrib(request,iat_id):
    tarib_id=request.GET['atrib_id']
    print(f"ID del atributo a borrar:{tarib_id}")

    target=Tatributos.objects.get(id=tarib_id)
    target.delete()
    messages.success(request,f'Atributo eliminado exitosamente!')
    return redirect('/config_02/'+str(iat_id))

def iat_new(request):
    if request.method=='GET':
        clientes=Cliente.objects.all()
        context = {        
        "accion":'new',
        "clientes":clientes
        }
        return render(request, 'iat.html', context)
    if request.method == "POST":
        testName=request.POST['testName']
        tipo=request.POST['tipo']
        if request.POST['cliente']=='otro':
            cliente_nuevo=request.POST['cliente_nuevo']
            target=Cliente.objects.create(nombre=cliente_nuevo)
        else:
        #el ciente puede ser antiguo
            cliente_id=request.POST['cliente']
            target=Cliente.objects.get(id=cliente_id)
    
        new_iat=Test.objects.create(cliente=target,nombre=testName,tipo=tipo)
    
        messages.success(request,f'Creación de nuevo IAT exitoso!')
        return redirect('/iat')  

def iat_edit(request,iat_id):
    if request.method=='GET':
        iat=Test.objects.get(id=iat_id)
        clientes=Cliente.objects.all()
        context={
            "iat":iat,
            "accion":'edit',
            "clientes":clientes
        }
        return render(request, 'iat.html', context)
    if request.method=='POST':
        testName=request.POST['testName']
        if request.POST['cliente']=='otro':
            cliente_nuevo=request.POST['cliente_nuevo']
            target=Cliente.objects.create(nombre=cliente_nuevo)
        else:
        #el ciente puede ser antiguo
            cliente_id=request.POST['cliente']
            target=Cliente.objects.get(id=cliente_id)
        iat=Test.objects.get(id=iat_id)
        iat.cliente=target
        iat.nombre=testName
        iat.save()
        messages.success(request,f'Modificación de IAT exitosa!')
        return redirect('/iat')

def iat_destroy(request,iat_id):    
    iat=Test.objects.get(id=iat_id).delete()
    messages.success(request,f'Eliminación de IAT exitosa!')
    
    return redirect('/iat')

def iat_add_cat(request,iat_id):
    iat=Test.objects.get(id=iat_id)
    if request.method=='GET':
        categorias=Categoria.objects.all()
        context={
            "iat":iat,
            "categorias":categorias
        }
        return render(request, 'iat_categorias.html', context)
    if request.method=='POST':
        
        if request.POST['categoria']=='otro':
            new_cat=request.POST['categoria_new']
            categoria=Categoria.objects.create(nombre=new_cat) 

        else:
            categoria=Categoria.objects.get(id=request.POST['categoria'])

        tcat=Tcategoria.objects.create(categoria=categoria,test=iat)
        
        return redirect('/iat')

def iat_detalle(request,iat_id): #analisis01
    iat=Test.objects.get(id=iat_id)
    caract=[]
    categoria="vacio"
    cars=[]
    tcat=[]
    combinaciones=[]
    participantes=[]
    if iat.categorias.count() > 0:
        tcat=Tcategoria.objects.get(id=iat.categorias.values_list('id')[0][0])
        categoria=Categoria.objects.get(id=iat.categorias.values_list('categoria_id')[0][0])
        result=tcat.car_cat.values_list('caracteristica_id')
        result2 =tcat.car_cat.values_list('id')
        i=0
        for r in result:
            c_aux=Caracteristica.objects.get(id=r[0])
            tcar=Tcaracteristicas.objects.get(id=result2[i][0])
            n_adj=tcar.adj_car.count()
            if tcar.analisis == 1:
                caract.append({"id": result2[i][0],"nombre":c_aux.nombre,"n_adj":n_adj,"analisis":tcar.analisis})
            i+=1
            
        cars=Caracteristica.objects.all()

        combinaciones=get_combinaciones_analisis01(iat_id)

        for c in iat.combinaciones.all():
            p={"nombre":c.participante.name,"user_id":c.participante.id}
            participantes.append(p)

        participantes=[dict(t) for t in {tuple(d.items()) for d in participantes}]
        
        #for x in participantes:
        #    print(x['nombre'])
        
        #resultados=Resultado.objects.filter(combinacion__test=iat)
        #print(resultados[0].combinacion.participante.name)
        

    context={
        "iat":iat,
        "accion":"detalle",
        "categoria": categoria,
        "tcat": tcat,
        "caract": caract,
        "cars": cars,
        "combinaciones":combinaciones,
        "participantes":participantes
    }
    return render(request, 'iat.html', context)

def config_cat(request,iat_id): #analisis03
    iat=Test.objects.get(id=iat_id)
    caract=[]
    categoria="vacio"
    cars=[]
    tcat=[]
    combinaciones=[]
    participantes=[]
    if iat.categorias.count() > 0:
        tcat=Tcategoria.objects.get(id=iat.categorias.values_list('id')[0][0])
        categoria=Categoria.objects.get(id=iat.categorias.values_list('categoria_id')[0][0])
        result=tcat.car_cat.values_list('caracteristica_id') # id de car
        result2 =tcat.car_cat.values_list('id') #id de  tcar
        print(result2)

        i=0
        for r in result:
            c_aux=Caracteristica.objects.get(id=r[0])
            tcar=Tcaracteristicas.objects.get(id=result2[i][0])
            #print(f"tcar:{tcar}")
            n_adj=tcar.adj_car.count()
            #id corresponde a tcat y nombre corresponde a car
            print(f"Valor a agregar:({result2[i][0]} ,{c_aux.nombre},{tcar.analisis})")
            if tcar.analisis == 3:
                caract.append({"id": result2[i][0],"nombre":c_aux.nombre,"n_adj":n_adj})
            i+=1
            
        cars=Caracteristica.objects.all()

        combinaciones=get_combinaciones_analisis03(iat_id)

        for c in iat.combinaciones.all():
            p={"nombre":c.participante.name,"user_id":c.participante.id}
            participantes.append(p)

        participantes=[dict(t) for t in {tuple(d.items()) for d in participantes}]
        
        #for x in participantes:
        #    print(x['nombre'])
        
        #resultados=Resultado.objects.filter(combinacion__test=iat)
        #print(resultados[0].combinacion.participante.name)
        

    context={
        "iat":iat,
        "accion":"detalle",
        "categoria": categoria,
        "tcat": tcat,
        "caract": caract,
        "cars": cars,
        "combinaciones":combinaciones,
        "participantes":participantes
    }
    print("go to config03")
    return render(request, 'config_analisis03.html', context)

def iat_add_car(request,iat_id):
    #falta validar que no se agregue 2 veces
    iat=Test.objects.get(id=iat_id)
    tcat=Tcategoria.objects.get(id=iat.categorias.values_list('id')[0][0])
    if request.POST['car'] =='otro':
        if request.POST['new_car'] == "":
            messages.warning(request,'La caracteristica no puede ser vacía')
            return redirect('/config_01/'+str(iat_id))
        else:    
            try:
                caract= Caracteristica.objects.create(nombre=request.POST['new_car'])
                messages.success(request,f'Caracteristica creada exitosamente!')
            except IntegrityError:
                messages.error(request,f'Esta caracteristica ya existe!')
                caract=Caracteristica.objects.get(nombre=request.POST['new_car'])         
    else:
        caract=Caracteristica.objects.get(id=request.POST['car']) 
    #agregamos la caract a la categoria
    #tcat.car_cat.nombre
    analisis_id=int(request.POST['analisis'])
    print(f"Analisis:{analisis_id}")
    new_car=Tcaracteristicas.objects.create(caracteristica=caract,categoria=tcat,analisis=analisis_id)
    new_car.analisis=analisis_id
    new_car.save()
    print(f"analisis:{new_car.analisis}")
    messages.success(request,f'Caracteristica agregada exitosamente!')
    
    return redirect('/config_0'+str(analisis_id)+'/'+str(iat_id))

def iat_rem_car(request,iat_id,analisis_id):
    tcar_id=request.GET['car_id']
    print(f"ID de la caracterista a borrar:{tcar_id}")

    target=Tcaracteristicas.objects.get(id=tcar_id)
    target.delete()

    
    messages.success(request,f'Caracteristica eliminada exitosamente!')
    return redirect('/config_0'+str(analisis_id)+'/'+str(iat_id))

def iat_add_calif(request,atrib_id):
    if request.method=='GET':
        tatrib=Tatributos.objects.get(id=atrib_id) #Atributo del test, con ID=atrib_id
        iat=tatrib.categoria.test #Test asociado al Atributo 
        
        adjs_list=Adjetivo.objects.all() # adjetivos/calificativos que se muestran en el combo para agregar
        calif=[] #lista de  diccionarios con los calificativos
        calif_totales=[] # lista con calificativos totales (sirve para hacer iterciones)
        tatrib=Tatributos.objects.get(id=atrib_id)
        n_calif=tatrib.calif_atrib.count()
        print(f"El atributo tiene {n_calif} calificativos")
        result=tatrib.calif_atrib.values_list('calificativo') #aca estan los ID de los ADJ
        result2 =tatrib.calif_atrib.values_list('id') #aca estan los ID de los T-ADJ
        if n_calif == 1: # si hay solo 1 queda en la posicion [0][0]
            adjetivo=Adjetivo.objects.get(id=result[0][0]) #con esto saco la descripcion del adjetivo
            #print(f"Adjetivo 1:{adjetivo}")
            calif.append({"nombre":adjetivo.nombre,"id":result2[0][0]}) #junto la descripcion con el ID del T-ADJ
            calif_totales.append(1)
        elif n_calif == 2: # si hay 2 quedan en las posiciones [0][0] y [1][0]
                
            adjetivo=Adjetivo.objects.get(id=result[0][0])    
            adjetivo2=Adjetivo.objects.get(id=result[1][0])
            #print(f"Adjetivo 1:{adjetivo.nombre}")
            #print(f"Adjetivo 2:{adjetivo2.nombre}")
            calif.append({"nombre":adjetivo.nombre,"id":result2[0][0]})
            calif.append({"nombre":adjetivo2.nombre,"id":result2[1][0]})
            #esto me sirve para que al mostrarlos pueda poner "Adjetivo n"
            calif_totales.append(1)
            calif_totales.append(2)


        context={
            "atrib":tatrib,
            "iat":iat,
            "adjs_list":adjs_list,
            "calif":calif,
            "calif_totales":calif_totales,
            "atributo":tatrib,
        }
        return render(request, 'iat_calificativo.html', context)
    if request.method=='POST':
        print(f"POST:{request.POST['adj_id']}")
        tatrib=Tatributos.objects.get(id=atrib_id)
        n_adj=tatrib.calif_atrib.count()
        adj_id= request.POST['adj_id']
        adjs_list=Adjetivo.objects.all()
        iat=tatrib.categoria.test
        if iat.tipo=="normal":
            if n_adj < 2:
                if adj_id == 'otro':
                    new_adj=request.POST['new_adj']
                    adj=Adjetivo.objects.create(nombre=new_adj)
                    messages.success(request,f'Nuevo adjetivo creado!')
                else:
                    #falta validacion para que no se repita
                    adj=Adjetivo.objects.get(id=adj_id)
                tadj=Tcalificativos.objects.create(calificativo=adj,atributo=tatrib)
                messages.success(request,f'Nuevo adjetivo añadido!')
            else:
                messages.warning(request,f'Cantidad de adjetivos máxima alcanzada!')
        


        return redirect('/config_02/calificativo/add/'+str(atrib_id))
    

def iat_rem_calif(request,calif_id):
    atrib_id= request.GET['atrib_id']
    target=Tcalificativos.objects.get(id=calif_id)
    target.delete()
    return redirect('/config_02/calificativo/add/'+str(atrib_id))

def iat_add_adj(request,car_id):

    if request.method=='GET':       
        tcar=Tcaracteristicas.objects.get(id=car_id) #Caracteristica del test, con ID=car_id
        iat=tcar.categoria.test #Test asociado a la Caracteristica del Test
        adjs_list=Adjetivo.objects.all() #Todos los Adjetivos que se mostraran en el combo
        #inicializacion de adjetivos
        adjs=[]
        adj_totales=[]
        #cuando es normal tiene 2 opciones (2 adjetivos maximo)
        if iat.tipo=="normal":
            #aca cuento los adjetivos que ya existen
            n_adj=tcar.adj_car.count()
            print(f"La caracteristica tiene {n_adj} adjetivos")
            result=tcar.adj_car.values_list('adjetivo') #aca estan los ID de los ADJ
            result2 =tcar.adj_car.values_list('id') #aca estan los ID de los T-ADJ

            if n_adj == 1: # si hay solo 1 queda en la posicion [0][0]
                adjetivo=Adjetivo.objects.get(id=result[0][0]) #con esto saco la descripcion del adjetivo
                #print(f"Adjetivo 1:{adjetivo}")
                adjs.append({"nombre":adjetivo.nombre,"id":result2[0][0]}) #junto la descripcion con el ID del T-ADJ
                adj_totales.append(1)
            elif n_adj == 2: # si hay 2 quedan en las posiciones [0][0] y [1][0]
                
                adjetivo=Adjetivo.objects.get(id=result[0][0])    
                adjetivo2=Adjetivo.objects.get(id=result[1][0])
                #print(f"Adjetivo 1:{adjetivo.nombre}")
                #print(f"Adjetivo 2:{adjetivo2.nombre}")
                adjs.append({"nombre":adjetivo.nombre,"id":result2[0][0]})
                adjs.append({"nombre":adjetivo2.nombre,"id":result2[1][0]})
                #esto me sirve para que al mostrarlos pueda poner "Adjetivo n"
                adj_totales.append(1)
                adj_totales.append(2)
        #en el caso de las elecciones son 6
        if iat.tipo=="elecciones2021":
            
            result=tcar.adj_car.values_list('adjetivo')
            result2 =tcar.adj_car.values_list('id')
            n_adj=tcar.adj_car.count()
            if n_adj > 0:
                adjetivo=Adjetivo.objects.get(id=result[0][0])
                adjs.append({"nombre":adjetivo.nombre,"id":result2[0][0]})
                adj_totales.append(1)            
            if n_adj > 1:
                adjetivo=Adjetivo.objects.get(id=result[1][0])
                adjs.append({"nombre":adjetivo.nombre,"id":result2[1][0]}) 
                adj_totales.append(2)        
            if n_adj > 2:
                adjetivo=Adjetivo.objects.get(id=result[2][0])
                adjs.append({"nombre":adjetivo.nombre,"id":result2[2][0]}) 
                adj_totales.append(3)
            if n_adj > 3:
                adjetivo=Adjetivo.objects.get(id=result[3][0])
                adjs.append({"nombre":adjetivo.nombre,"id":result2[3][0]}) 
                adj_totales.append(4)
            if n_adj > 4:
                adjetivo=Adjetivo.objects.get(id=result[4][0])
                adjs.append({"nombre":adjetivo.nombre,"id":result2[4][0]}) 
                adj_totales.append(5)
            if n_adj > 5:
                adjetivo=Adjetivo.objects.get(id=result[5][0])
                adjs.append({"nombre":adjetivo.nombre,"id":result2[5][0]}) 
                adj_totales.append(6)
        #en otro caso puede tener mas     
        else:
            pass

        # if tcar
        total_adjetivos=len(adj_totales)
        context={
            "car":tcar,
            "iat":iat,
            "adjs_list":adjs_list,
            "adjs":adjs,
            "adj_totales":adj_totales,
            "total_adjetivos":total_adjetivos
        }
        return render(request, 'iat_adjetivo.html', context)
    if request.method=='POST':
        print(f"POST:{request.POST['adj_id']}")
        tcar=Tcaracteristicas.objects.get(id=car_id)
        n_adj=tcar.adj_car.count()
        adj_id= request.POST['adj_id']
        adjs_list=Adjetivo.objects.all()
        iat=tcar.categoria.test
        if iat.tipo=="normal":
            if n_adj < 2:
                if adj_id == 'otro':
                    new_adj=request.POST['new_adj']
                    adj=Adjetivo.objects.create(nombre=new_adj)
                    messages.success(request,f'Nuevo adjetivo creado!')
                else:
                    adj=Adjetivo.objects.get(id=adj_id)
                tadj=Tadjetivos.objects.create(adjetivo=adj,caracteristica=tcar)
                messages.success(request,f'Nuevo adjetivo añadido!')
            else:
                messages.warning(request,f'Cantidad de adjetivos máxima alcanzada!')
        if iat.tipo=="elecciones2021":
            if adj_id == 'otro':
                    new_adj=request.POST['new_adj']
                    adj=Adjetivo.objects.create(nombre=new_adj)
                    messages.success(request,f'Nuevo adjetivo creado!')
            else:
                adj=Adjetivo.objects.get(id=adj_id)
            tadj=Tadjetivos.objects.create(adjetivo=adj,caracteristica=tcar)
            messages.success(request,f'Nuevo adjetivo añadido!')
        return redirect('/iat/adjetivo/add/'+str(car_id))
        
def iat_rem_adj(request,adj_id):
    car_id= request.GET['car_id']
    target=Tadjetivos.objects.get(id=adj_id)
    target.delete()
    return redirect('/iat/adjetivo/add/'+str(car_id))

def test(request,test_id):
    #inicio del test, generamos las combinaciones
    #las metemos en una variable de sesion
    #generamos un objeto para guardar los resultados
    t_id=test_id
    request.session['iat_id']=t_id
    #request.session['user_id']=1
    request.session['analisis01']=get_combinaciones_analisis01(t_id)
    print(f"USER_ID:{request.session['user']['id']}")
    request.session['user_id']=request.session['user']['id']
    save_combinaciones(request.session['analisis01'],t_id,request.session['user']['id'],1)

    #esto esta incompleto
    request.session['analisis02']=get_combinaciones_analisis02(t_id)
    request.session['analisis03']=get_combinaciones_analisis03(t_id)
    request.session['analisis04']=get_combinaciones_analisis04(t_id)
    
    context = {
        'saludo': 'Hola'
    }
    return render(request, 'inicio.html', context)

def paso1(request):
    #analisis de categoria
    
    if request.method == "POST":
        milisegundos=request.POST['milisegundos']
        combinacion_id=request.POST['combinacion']
        analisis=request.POST['analisis']
        opcion=request.POST['opcion']
        test=Test.objects.get(id=request.POST['iat_id'])
        user=User.objects.get(id=request.POST['user_id'])        
        print(f"pos:{combinacion_id} , analisis:{analisis},test:{request.POST['iat_id']},user:{request.POST['user_id']},opcion:{opcion}")
        combi=Combinacion.objects.filter(indice=combinacion_id,analisis=analisis,test=test,participante=user)
        #print("combinaciones:")
        #print(combi.count())
        for c in combi:
            print("c:")
            print(c)
        #Respuesta
            res=Resultado.objects.create(combinacion=c,milisegundos=milisegundos,opcion=opcion)    

    #a)pedimos 1 combinacion al azar
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
        return render(request, 'primera_parte.html', context)
    else:
        return redirect('/test/paso2')

def paso2(request):
    #se acabo la lista de analisis01 y empezamos con la lista analisis02
    pass

    context = {        
    }
    return render(request, 'segunda_parte.html', context)

def paso3(request):
    context = {        
    }
    return render(request, 'tercera_parte.html', context)

def paso4(request):
    context = {        
    }
    return render(request, 'cuarta_parte.html', context)

def final(request):
    context = {        
    }
    return render(request, 'final.html', context)

