#from .models import Test,Cliente,Categoria,Tcategoria,Caracteristica,Tcaracteristicas,Adjetivo,Tadjetivos,User,Combinacion,Resultado, Sondeo, Producto,Tproductos, Tatributos,Tcalificativos
from .models.sondeo import Sondeo
from .models.descarga import Descargas
from .models.user import User
from .models.test import Test
#from .models.cliente import Cliente
#from .models.comuna import Comuna
#from .models.provincia import Provincia
#from .models.region import Region
from .models.categoria import Categoria, Tcategoria
from .models.caracteristica import Caracteristica, Tcaracteristicas, Tatributos
from .models.adjetivo import Adjetivo, Tadjetivos
from .models.producto import Producto, Tproductos
from .models.combinacion import Combinacion
from .models.resultado import Resultado


def get_combinaciones_analisis01(iat_id):
    iat=Test.objects.get(id=iat_id)
    c=[]
    print(f'iat.categorias.count():{iat.categorias.count()}')
    if iat.categorias.count() > 0:
        tcat=Tcategoria.objects.get(id=iat.categorias.values_list('id')[0][0])
        categoria=Categoria.objects.get(id=iat.categorias.values_list('categoria_id')[0][0])
        print(f'tcat.car_cat.count():{tcat.car_cat.count()}')
        if tcat.car_cat.count() > 0:
            car_ids=tcat.car_cat.values_list('caracteristica_id')
            tcar_ids =tcat.car_cat.values_list('id')
            i=0
            pos=0
            for r in car_ids:                
                c_aux=Caracteristica.objects.get(id=r[0])
                tcar=Tcaracteristicas.objects.get(id=tcar_ids[i][0])
                print(f'tcar.adj_car.count():{tcar.adj_car.count()}')
                if tcar.adj_car.count() > 0:
                    adj=tcar.adj_car.values_list('adjetivo_id')
                    tadj=tcar.adj_car.values_list('id')
                    if tcar.adj_car.count() == 1:
                        if tcar.analisis == 1:
                            adj1=Adjetivo.objects.get(id=adj[0][0]) 
                            c.append({"iat":iat.nombre,"cat":categoria.nombre,"car":c_aux.nombre,"adj1":adj1,"adj2":"","tadj1":tadj[0][0],"tadj2":""})
                    elif tcar.adj_car.count() == 2:
                        #caract.append({"id": tcar_ids[i][0],"nombre":c_aux.nombre})
                        #print(f"analisis:{tcar.analisis}")
                        if tcar.analisis == 1:
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

def get_combinaciones_analisis02(iat_id): #analisis producto-marca-servicio
    #para este analisis se necesita PRODUCTO - CARACTERISTICA - ADJETIVOS
    '''
    { 
    "iat":
    "producto_i":
    "caracteristica_j":
    "adjetivo1":
    "adjetivo2":
    }
    ''' 
    iat=Test.objects.get(id=iat_id)
    combinaciones=[]
    # obtenemos la categoria
    if iat.categorias.count() > 0:
        tcat=Tcategoria.objects.get(id=iat.categorias.values_list('id')[0][0])
        #categoria=Categoria.objects.get(id=iat.categorias.values_list('categoria_id')[0][0])
        categoria=tcat.categoria
        #print(categoria)
        #desde la tcategoria obtenemos los productos y los atributos
        tprods=tcat.prod_cat.all()
        print(f"cantidad de productos:{tprods.count()}")
        #tprods=Tproductos.prod_cat.values_list()
        tabribs=tcat.atr_cat.all()
        print(f"cantidad de atributos:{tabribs.count()}")
        pos=0
        for tprod in tprods:
            print(f"procesando producto:{tprod.producto.nombre}")
            for tatrib in tabribs:
                print(f"    procesando atributo:{tatrib.caracteristica.nombre}")
                califs=tatrib.calif_atrib.all()
                print(f"    cantidad de Calificativos:{califs.count()}")
                if califs.count() == 1:
                    print(f"    calif_1:{califs.first()}")
                    combi={
                        "iat":iat.nombre,
                            "producto":tprod.producto.nombre,
                            "atributo":tatrib.caracteristica.nombre,
                            "adj1":califs.first().calificativo.nombre,
                            "adj2":"",
                            "tadj1":califs.first().id,
                            "tadj2":"",
                            "pos":pos,
                        }
                    pos+=1
                    combinaciones.append(combi)
                elif califs.count() == 2:
                    print(f"\tcalif_1:{califs.first()}")
                    print(f"\tcalif_2:{califs.last()}")
                    combi={
                    "iat":iat.nombre,
                        "producto":tprod.producto.nombre,
                        "atributo":tatrib.caracteristica.nombre,
                        "adj1":califs.first().calificativo.nombre,
                        "adj2":califs.last().calificativo.nombre,
                        "tadj1":califs.first().id,
                        "tadj2":califs.last().id,
                        "pos":pos
                    }
                    pos+=1
                    combinaciones.append(combi)
                    combi={
                    "iat":iat.nombre,
                        "producto":tprod.producto.nombre,
                        "atributo":tatrib.caracteristica.nombre,
                        "adj1":califs.last().calificativo.nombre,
                        "adj2":califs.first().calificativo.nombre,
                        "tadj1":califs.last().id,
                        "tadj2":califs.first().id,
                        "pos":pos
                    }
                    pos+=1
                    combinaciones.append(combi)    
                #print(combinaciones)
    return combinaciones

def get_combinaciones_analisis03(iat_id):
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
                #print(tcar.analisis)
                if tcar.analisis == 3:
                    #print(tcar.analisis)
                    if tcar.adj_car.count() > 0 :
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

def get_combinaciones_analisis04(iat_id):
    pass

def save_combinaciones(combis,test_id,user_id,analisis_id):
    test=Test.objects.get(id=test_id)
    participante=User.objects.get(id=user_id)
    index=0
    
    #revisamos si no existe y si no guardamos
    c_test=Combinacion.objects.filter(test=test,participante=participante,analisis=analisis_id)
    #cambiamos a 1 para borrar las combinaciones y probar otra vez
    borrar=0
    if borrar == 1:
        c_test.delete()        
        print("se borraron las combinaciones")
        
    if c_test.count()>0:
        print("combinaciones ya existen para ese test, analisis y usuario")
    else:
        print("combinaciones no existen para ese test, analisis y usuario, se agregan")        
        for c in combis:
            #guardamos los registros            
            Combinacion.objects.create(test=test,participante=participante,indice=index,valor=c,analisis=analisis_id)
            index+=1
        print(f"Se guardaron {index} registros ")


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
                max_adj=tcar.adj_car.count()
                #print(f"ADJ_MAX:{max_adj}")
                if tcar.adj_car.count() > 0:
                    adj=tcar.adj_car.values_list('adjetivo_id')
                    tadj=tcar.adj_car.values_list('id')
                    #aca van las combinaciones por adjetivos 1-2, 3-4, 5-6
                    dict_comb={"iat":iat.nombre,"cat":categoria.nombre,"car":c_aux.nombre}
                    dict_comb_2={"iat":iat.nombre,"cat":categoria.nombre,"car":c_aux.nombre}
                    '''
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
                    '''
                    if max_adj >= 2:
                        adj1 = Adjetivo.objects.get(id=adj[0][0])
                        dict_comb["adj1"]  = adj1.nombre
                        dict_comb["tadj1"] = tadj[0][0]
                        dict_comb["img1"]  = adj1.nombre + ".JPG"
                        dict_comb["pos"]   = pos

                        adj2 = Adjetivo.objects.get(id=adj[1][0])
                        dict_comb["adj2"]  = adj2.nombre
                        dict_comb["tadj2"] = tadj[1][0]
                        dict_comb["img2"]  = adj2.nombre + ".JPG"
                        pos += 1

                        # Invertida
                        dict_comb_2["adj1"]  = adj2.nombre
                        dict_comb_2["tadj1"] = tadj[1][0]
                        dict_comb_2["img1"]  = adj2.nombre + ".JPG"
                        dict_comb_2["adj2"]  = adj1.nombre
                        dict_comb_2["tadj2"] = tadj[0][0]
                        dict_comb_2["img2"]  = adj1.nombre + ".JPG"
                        dict_comb_2["pos"]   = pos
                        pos += 1

                    if max_adj >= 4:
                        adj3 = Adjetivo.objects.get(id=adj[2][0])
                        adj4 = Adjetivo.objects.get(id=adj[3][0])

                        dict_comb["adj3"]  = adj3.nombre
                        dict_comb["tadj3"] = tadj[2][0]
                        dict_comb["img3"]  = adj3.nombre + ".JPG"
                        dict_comb["adj4"]  = adj4.nombre
                        dict_comb["tadj4"] = tadj[3][0]
                        dict_comb["img4"]  = adj4.nombre + ".JPG"

                        dict_comb_2["adj3"]  = adj4.nombre
                        dict_comb_2["tadj3"] = tadj[3][0]
                        dict_comb_2["img3"]  = adj4.nombre + ".JPG"
                        dict_comb_2["adj4"]  = adj3.nombre
                        dict_comb_2["tadj4"] = tadj[2][0]
                        dict_comb_2["img4"]  = adj3.nombre + ".JPG"

                    if max_adj >= 6:
                        adj5 = Adjetivo.objects.get(id=adj[4][0])
                        adj6 = Adjetivo.objects.get(id=adj[5][0])

                        dict_comb["adj5"]  = adj5.nombre
                        dict_comb["tadj5"] = tadj[4][0]
                        dict_comb["img5"]  = adj5.nombre + ".JPG"
                        dict_comb["adj6"]  = adj6.nombre
                        dict_comb["tadj6"] = tadj[5][0]
                        dict_comb["img6"]  = adj6.nombre + ".JPG"

                        dict_comb_2["adj5"]  = adj6.nombre
                        dict_comb_2["tadj5"] = tadj[5][0]
                        dict_comb_2["img5"]  = adj6.nombre + ".JPG"
                        dict_comb_2["adj6"]  = adj5.nombre
                        dict_comb_2["tadj6"] = tadj[4][0]
                        dict_comb_2["img6"]  = adj5.nombre + ".JPG"

                    # Guardar copias finales (para evitar mutaciones posteriores)
                    c.append(dict_comb.copy())
                    c.append(dict_comb_2.copy())
                    
                i+=1

    return c

    iat=Test.objects.get(id=iat_id)
    c=[]
    print(f'iat.categorias.count():{iat.categorias.count()}')
    if iat.categorias.count() > 0:
        tcat=Tcategoria.objects.get(id=iat.categorias.values_list('id')[0][0])
        categoria=Categoria.objects.get(id=iat.categorias.values_list('categoria_id')[0][0])
        print(f'tcat.car_cat.count():{tcat.car_cat.count()}')
        if tcat.car_cat.count() > 0:
            car_ids=tcat.car_cat.values_list('caracteristica_id')
            tcar_ids =tcat.car_cat.values_list('id')
            i=0
            pos=0
            for r in car_ids:                
                c_aux=Caracteristica.objects.get(id=r[0])
                tcar=Tcaracteristicas.objects.get(id=tcar_ids[i][0])
                max_adj=tcar.adj_car.count()
                print(f"ADJ_MAX:{max_adj}")
                print(f'tcar.adj_car.count():{tcar.adj_car.count()}')
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
    print(f"#combis :{c}")
    return c