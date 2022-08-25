from django.urls import path
from . import views,auth,elecciones2021,resumen, elecciones
from .vistas import categoria,cliente,producto,caracteristica,adjetivo,iat,usuarios,sondeo

urlpatterns = [
    path('', views.index_resultados), # se comenta cuando hay test activo
    path('descarga', views.descarga_resultados),
    #path('', views.index),# se descomenta cuando hay test activo
    path('registro', auth.registro),
    path('login', auth.login),
    path('logout', auth.logout),
    #ejecucion
    path('test/<int:test_id>', iat.test),
    path('test/paso1', iat.paso1),
    path('test/paso2', iat.paso2),
    path('test/paso3', iat.paso3),
    path('test/paso4', iat.paso4),
    path('test/paso5', iat.paso5),
    path('test/final', iat.final),
    #mantenedores
    path('cliente/', cliente.cliente), 
    path('cliente/new', cliente.cliente_new), 
    path('cliente/<int:cli_id>/edit', cliente.cliente_edit), 
    path('cliente/<int:cli_id>/destroy', cliente.cliente_destroy), 

    path('categoria/', categoria.categorias), 
    path('categoria/new', categoria.categorias_new), 
    path('categoria/<int:cat_id>/edit', categoria.categorias_edit), 
    path('categoria/<int:cat_id>/destroy', categoria.categorias_destroy), 

    path('producto/', producto.producto),
    path('producto/new', producto.producto_new),  
    path('producto/<int:prod_id>/edit', producto.producto_edit),
    path('producto/<int:prod_id>/destroy', producto.producto_destroy), 

    path('caracteristica/', caracteristica.caracteristica),
    path('caracteristica/new', caracteristica.caracteristica_new),  
    path('caracteristica/<int:car_id>/edit', caracteristica.caracteristica_edit),
    path('caracteristica/<int:car_id>/destroy', caracteristica.caracteristica_destroy), 

    path('adjetivo/', adjetivo.adjetivo),
    path('adjetivo/new', adjetivo.adjetivo_new),  
    path('adjetivo/<int:adj_id>/edit', adjetivo.adjetivo_edit),
    path('adjetivo/<int:adj_id>/destroy', adjetivo.adjetivo_destroy), 

    # creacion de test
    path('iat/', iat.iat ), 
    path('iat/new', iat.iat_new), 
    path('iat/<int:iat_id>/edit', iat.iat_edit), 
    path('iat/<int:iat_id>/destroy', iat.iat_destroy),
    path('iat/<int:iat_id>', iat.iat_detalle ), 
    
    ### analisis categoria 
    path('iat/categoria/add/<int:iat_id>', iat.iat_add_cat),
    path('iat/caracteristica/add/<int:iat_id>', iat.iat_add_car),
    path('iat/caracteristica/remove/<int:iat_id>', iat.iat_rem_car),
    path('iat/adjetivo/add/<int:car_id>', iat.iat_add_adj),
    path('iat/adjetivo/remove/<int:adj_id>', iat.iat_rem_adj),

    path('iat/resultado/<int:iat_id>/<int:user_id>', views.resultado), 
    #iat elecciones 2021
    path('elecciones2021/start/<int:iat_id>', elecciones2021.elecciones_start),
    path('elecciones2021/test/<str:disp>', elecciones2021.elecciones_test), 
    path('elecciones2021/end', elecciones2021.elecciones_end), 
    path('elecciones2021/regresar', elecciones2021.regresar), 
    path('elecciones2021/instrucciones', elecciones2021.instrucciones),  
    #iat elecciones 2022
    path('elecciones2022/start/<int:iat_id>', elecciones.elecciones_start),
    path('elecciones2022/test/<str:disp>', elecciones.elecciones_test), 
    path('elecciones2022/end', elecciones.elecciones_end), 
    path('elecciones2022/regresar', elecciones.regresar), 
    path('elecciones2022/instrucciones', elecciones.instrucciones),  

    path('usuarios', usuarios.usuarios), 
    path('usuarios/<int:user_id>', usuarios.usuarios_detalle),  

    path('sondeos', sondeo.sondeos), 
    path('sondeos/activar', sondeo.sondeos), 
    path('sondeos/desactivar/<int:s_id>', sondeo.sondeos_deactivate), 
    path('sondeos/<int:s_id>/destroy', sondeo.sondeos_destroy), 

    path('resumen/<int:iat_id>', resumen.resumen), 

]
