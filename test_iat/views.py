from django.core.checks import messages
from django.shortcuts import render, HttpResponse,redirect
from .models import Categoria, Cliente, Tcaracteristicas, Tcategoria,Test,Caracteristica,Adjetivo, Producto, Tadjetivos, User, Combinacion, Resultado
from django.contrib import messages
from django.db import IntegrityError
import random

# funcion para generar las combinaciones del analisis 1
def get_combinaciones_analisis01(iat_id):
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
                    if tcar.adj_car.count() == 1:
                        adj1=Adjetivo.objects.get(id=adj[0][0]) 
                        c.append({"iat":iat.nombre,"cat":categoria.nombre,"car":c_aux.nombre,"adj1":adj1,"adj2":"","tadj1":tadj[0][0],"tadj2":""})
                    elif tcar.adj_car.count() == 2:
                        #caract.append({"id": tcar_ids[i][0],"nombre":c_aux.nombre})
                        adj1=Adjetivo.objects.get(id=adj[0][0])  
                        adj2=Adjetivo.objects.get(id=adj[1][0])                         
                        c.append({"iat":iat.nombre,"cat":categoria.nombre,"car":c_aux.nombre,"adj1":adj1.nombre,"adj2":adj2.nombre,"tadj1":tadj[0][0],"tadj2":tadj[1][0],"pos":pos})
                        pos+=1
                        c.append({"iat":iat.nombre,"cat":categoria.nombre,"car":c_aux.nombre,"adj1":adj2.nombre,"adj2":adj1.nombre,"tadj1":tadj[1][0],"tadj2":tadj[0][0],"pos":pos})
                        pos+=1
                else: # Caso cuando no tiene adjetivos 
                    c.append({"iat":iat.nombre,"cat":categoria.nombre,"car":c_aux.nombre,"adj1":"","adj2":"","tadj1":"","tadj2":""})
                i+=1

    return c

def get_combinaciones_analisis02(iat_id):
    pass
def get_combinaciones_analisis03(iat_id):
    pass

def get_combinaciones_analisis04(iat_id):
    pass

def index(request):
    context = {
        'saludo': 'Hola'
    }
    #Combinacion.objects.all().delete()
    #Resultado.objects.all().delete()
    return render(request, 'index.html', context)

def login(request):
    context = {
        'saludo': 'Hola'
    }
    return render(request, 'login.html', context)
def registro(request):
    context = {
        'saludo': 'Hola'
    }
    return render(request, 'registro.html', context)

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
    

def test(request,test_id):
    #inicio del test, generamos las combinaciones
    #las metemos en una variable de sesion
    #generamos un objeto para guardar los resultados
    t_id=5
    request.session['iat_id']=t_id
    #request.session['user_id']=1
    request.session['analisis01']=get_combinaciones_analisis01(5)
    
    save_combinaciones(request.session['analisis01'],t_id,request.session['user_id'],1)

    request.session['analisis02']=get_combinaciones_analisis02(5)
    request.session['analisis03']=get_combinaciones_analisis03(5)
    request.session['analisis04']=get_combinaciones_analisis04(5)
    

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

def paso5(request):
    context = {        
    }
    return render(request, 'quinta_parte.html', context)

def final(request):
    context = {        
    }
    return render(request, 'final.html', context)

## MANTENEDORES
#CLIENTE
def cliente(request):
    clientes= Cliente.objects.all()
    context = {        
    "clientes":clientes,
    "accion":'default'
    }
    return render(request, 'clientes.html', context)


def cliente_new(request):
    if request.method=='GET':
        context = {        
        "accion":'new'
        }
        return render(request, 'clientes.html', context)
    if request.method == "POST":
        cli=request.POST['cliente']
        Cliente.objects.create(nombre=cli)
        messages.success(request,f'Creación de Cliente exitosa!')
        clientes= Cliente.objects.all()
        context = {        
        "clientes":clientes,
        "accion":'default'
        }
        return redirect('/cliente')

def cliente_edit(request,cli_id):
    if request.method=='GET':
        cli=Cliente.objects.get(id=cli_id)
        context = {    
            "cli":cli,    
            "accion":'edit'
        }
        return render(request, 'clientes.html', context)
    if request.method == "POST":
        cli=Cliente.objects.get(id=cli_id)
        cli.nombre=request.POST['cliente']
        cli.save()
        messages.success(request,f'Modificación de Cliente exitosa!')
        return redirect('/cliente')

def cliente_destroy(request,cli_id):
    Cliente.objects.get(id=cli_id).delete()
    messages.success(request,f'Cliente eliminado con exito!')
    return redirect('/cliente')


#CATEGORIAS
def categorias(request):
    categorias= Categoria.objects.all()
    context = {        
    "categorias":categorias,
    "accion":'default'
    }
    return render(request, 'categorias.html', context)


def categorias_new(request):
    if request.method=='GET':
        context = {        
        "accion":'new'
        }
        return render(request, 'categorias.html', context)
    if request.method == "POST":
        cat=request.POST['categoria']
        Categoria.objects.create(nombre=cat)
        messages.success(request,f'Creación de Categoria exitosa!')
        categorias= Categoria.objects.all()
        context = {        
        "categorias":categorias,
        "accion":'default'
        }
        return redirect('/categoria')

def categorias_edit(request,cat_id):
    if request.method=='GET':
        cat=Categoria.objects.get(id=cat_id)
        context = {    
            "cat":cat,    
            "accion":'edit'
        }
        return render(request, 'categorias.html', context)
    if request.method == "POST":
        cat=Categoria.objects.get(id=cat_id)
        cat.nombre=request.POST['categoria']
        cat.save()
        messages.success(request,f'Modificación de Categoria exitosa!')
        return redirect('/categoria')

def categorias_destroy(request,cat_id):
    Categoria.objects.get(id=cat_id).delete()
    messages.success(request,f'Categoria eliminada con exito!')
    return redirect('/categoria')

#PRODUCTOS
def producto(request):
    productos= Producto.objects.all()
    context = {        
    "productos":productos,
    "accion":'default'
    }
    return render(request, 'productos.html', context)


def producto_new(request):
    if request.method=='GET':
        context = {        
        "accion":'new'
        }
        return render(request, 'productos.html', context)
    if request.method == "POST":
        prod=request.POST['producto']
        Producto.objects.create(nombre=prod)
        messages.success(request,f'Creación de Producto exitosa!')
        productos= Producto.objects.all()
        context = {        
        "productos":productos,
        "accion":'default'
        }
        return redirect('/producto')

def producto_edit(request,prod_id):
    if request.method=='GET':
        prod=Producto.objects.get(id=prod_id)
        context = {    
            "prod":prod,    
            "accion":'edit'
        }
        return render(request, 'productos.html', context)
    if request.method == "POST":
        prod=Producto.objects.get(id=prod_id)
        prod.nombre=request.POST['producto']
        prod.save()
        messages.success(request,f'Modificación de Producto exitosa!')
        return redirect('/producto')

def producto_destroy(request,prod_id):
    Producto.objects.get(id=prod_id).delete()
    messages.success(request,f'Producto eliminado con exito!')
    return redirect('/producto')

#CARACTERISTICAS
def caracteristica(request):
    caracteristicas= Caracteristica.objects.all()
    context = {        
    "caracteristicas":caracteristicas,
    "accion":'default'
    }
    return render(request, 'caracteristicas.html', context)

def caracteristica_new(request):
    if request.method=='GET':
        context = {        
        "accion":'new'
        }
        return render(request, 'caracteristicas.html', context)
    if request.method == "POST":
        car=request.POST['caracteristica']
        Caracteristica.objects.create(nombre=car)
        messages.success(request,f'Creación de Caracteristica exitosa!')
        caracteristicas= Caracteristica.objects.all()
        context = {        
        "caracteristicas":caracteristicas,
        "accion":'default'
        }
        return redirect('/caracteristica')

def caracteristica_edit(request,car_id):
    if request.method=='GET':
        car=Caracteristica.objects.get(id=car_id)
        context = {    
            "car":car,    
            "accion":'edit'
        }
        return render(request, 'caracteristicas.html', context)
    if request.method == "POST":
        Car=Caracteristica.objects.get(id=car_id)
        Car.nombre=request.POST['caracteristica']
        Car.save()
        messages.success(request,f'Modificación de Caracteristica exitosa!')
        return redirect('/caracteristica')

def caracteristica_destroy(request,car_id):
    Caracteristica.objects.get(id=car_id).delete()
    messages.success(request,f'Caracteristica eliminado con exito!')
    return redirect('/caracteristica')

#ADJETIVOS
def adjetivo(request):
    adjetivos= Adjetivo.objects.all()
    context = {        
    "adjetivos":adjetivos,
    "accion":'default'
    }
    return render(request, 'adjetivos.html', context)


def adjetivo_new(request):
    if request.method=='GET':
        context = {        
        "accion":'new'
        }
        return render(request, 'adjetivos.html', context)
    if request.method == "POST":
        adj=request.POST['adjetivo']
        try:
            Adjetivo.objects.create(nombre=adj)
            messages.success(request,f'Creación de Adjetivo exitosa!')
        except IntegrityError:
            messages.error(request,f'Este Adjetivo ya existe!')
        
        adjetivos= Adjetivo.objects.all()
        context = {        
        "adjetivos":adjetivos,
        "accion":'default'
        }
        return redirect('/adjetivo')

def adjetivo_edit(request,adj_id):
    if request.method=='GET':
        adj=Adjetivo.objects.get(id=adj_id)
        context = {    
            "adj":adj,    
            "accion":'edit'
        }
        return render(request, 'adjetivos.html', context)
    if request.method == "POST":
        adj=Adjetivo.objects.get(id=adj_id)
        adj.nombre=request.POST['adjetivo']
        try:
            adj.save()
            messages.success(request,f'Modificación de Adjetivo exitosa!')
        except IntegrityError:
            messages.error(request,f'Este Adjetivo ya existe, no se puede modificar!')
        
        return redirect('/adjetivo')

def adjetivo_destroy(request,adj_id):
    Adjetivo.objects.get(id=adj_id).delete()
    messages.success(request,f'Adjetivo eliminado con exito!')
    return redirect('/adjetivo')

#Creación de nuevo test:
def iat(request):
    iats=Test.objects.all()
    context={
        "iats":iats,
        "accion":'default'
    }
    return render(request, 'iat.html', context)

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
        if request.POST['cliente']=='otro':
            cliente_nuevo=request.POST['cliente_nuevo']
            target=Cliente.objects.create(nombre=cliente_nuevo)
        else:
        #el ciente puede ser antiguo
            cliente_id=request.POST['cliente']
            target=Cliente.objects.get(id=cliente_id)
    
        new_iat=Test.objects.create(cliente=target,nombre=testName)
    
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

def iat_detalle(request,iat_id):
    iat=Test.objects.get(id=iat_id)
    caract=[]
    categoria="vacio"
    cars=[]
    tcat=[]
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
            caract.append({"id": result2[i][0],"nombre":c_aux.nombre,"n_adj":n_adj})
            i+=1
            
        cars=Caracteristica.objects.all()

        combinaciones=get_combinaciones_analisis01(iat_id)
        participantes=[]
        for c in iat.combinaciones.all():
            p={"nombre":c.participante.name,"user_id":c.participante.id}
            participantes.append(p)
        
        participantes=[dict(t) for t in {tuple(d.items()) for d in participantes}]
        
        for x in participantes:
            print(x['nombre'])
        #resultados=Resultado.objects.filter(combinacion__test=iat)
        #print(resultados[0].combinacion.participante.name)
        par=[]
        


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

def iat_add_car(request,iat_id):
    #falta validar que no se agregue 2 veces
    iat=Test.objects.get(id=iat_id)
    tcat=Tcategoria.objects.get(id=iat.categorias.values_list('id')[0][0])
    if request.POST['car'] =='otro':
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


    new_car=Tcaracteristicas.objects.create(caracteristica=caract,categoria=tcat)
    messages.success(request,f'Caracteristica agregada exitosamente!')
    
    return redirect('/iat/'+str(iat_id))

def iat_rem_car(request,iat_id):
    tcar_id=request.GET['car_id']
    target=Tcaracteristicas.objects.get(id=tcar_id)
    target.delete()
    messages.success(request,f'Caracteristica eliminada exitosamente!')
    return redirect('/iat/'+str(iat_id))

def iat_add_adj(request,car_id):
    if request.method=='GET':       
        tcar=Tcaracteristicas.objects.get(id=car_id)
        iat=tcar.categoria.test
        adjs_list=Adjetivo.objects.all()
        adj1={"nombre":"Sin asignar","id":-1}
        adj2={"nombre":"Sin asignar","id":-1}
        #aca cuento los adjetivos que ya existen
        n_adj=tcar.adj_car.count()
        result=tcar.adj_car.values_list('adjetivo')
        result2 =tcar.adj_car.values_list('id')

        if n_adj == 1:
            adjetivo=Adjetivo.objects.get(id=result[0][0])
            adj1={"nombre":adjetivo.nombre,"id":result2[0][0]}
        elif n_adj == 2:
            adjetivo=Adjetivo.objects.get(id=result[0][0])    
            adj1={"nombre":adjetivo.nombre,"id":result2[0][0]}
            adjetivo=Adjetivo.objects.get(id=result[1][0])
            adj2={"nombre":adjetivo.nombre,"id":result2[1][0]}
        # if tcar
        context={
            "car":tcar,
            "iat":iat,
            "adjs_list":adjs_list,
            "adj1":adj1,
            "adj2":adj2
        }
        return render(request, 'iat_adjetivo.html', context)
    if request.method=='POST':
        
        tcar=Tcaracteristicas.objects.get(id=car_id)
        n_adj=tcar.adj_car.count()
        adj_id= request.POST['adj_id']
        adjs_list=Adjetivo.objects.all()
        iat=tcar.categoria.test
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

        return redirect('/iat/adjetivo/add/'+str(car_id))
        
def iat_rem_adj(request,adj_id):
    car_id= request.GET['car_id']
    target=Tadjetivos.objects.get(id=adj_id)
    target.delete()
    return redirect('/iat/adjetivo/add/'+str(car_id))

def resultado(request,iat_id,user_id):
    iat=Test.objects.get(id=iat_id)
    participante=User.objects.get(id=user_id)
    resultados=Resultado.objects.filter(combinacion__test=iat,combinacion__participante=participante)
    
    print(resultado)
    context={
        "resultados":resultados
        }
    return render(request, 'resultado.html', context)
