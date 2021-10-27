
let start=0;
let end=0;
let  eventoControlado = false;

const hrtime =
    (typeof window !== 'undefined' &&
    typeof window.performance !== 'undefined' &&
    window.performance.now) ?
        window.performance.now.bind (window.performance) :
        (typeof require !== 'undefined') ?
        require ('perf_hooks').performance.now :
        function () {
            var h = process.hrtime ();
            return (h[ 0 ] + (h[ 1 ] / 1e9)) * 1000;
        };

$( document ).ready(function() {
    console.log( "ready!" );
	start = hrtime (); 
	
	$('#escribe').focus();
	$("#escribe").keydown(function(event){
		if(event.which==69){
			$("#parrafo").text("presionó la tecla e");
			detener_tiempo("1");
			}
		if(event.which==73){
			$("#parrafo").text("presionó la tecla i");
			detener_tiempo("2");
			}	
		$("#escribe").val("");
	}); 
	
});

$('body').on('click',function(){
    console.log('fuera del focus');
    $('#escribe').focus();
})

function detener_tiempo(opcion){
    end   =  hrtime ();
    delta=end-start;
    resultado='Tiempo transcurrido:'+(delta)+' Milisegundos <br>';
   // $('#resultado').append(resultado);
    $('#milisegundos').val(delta);
    $('#opcion').val(opcion);
    //alert("opcion:",opcion)
    //console.log ('start:', start, 'end:', end, 'Diferencia:',end-start);
    $('#form_tiempo').submit();
    }

$('.stop-button').on( "click", function() {
    end   =  hrtime ();
    nombre=$(this).attr('id')
    resultado=nombre+', tiempo transcurrido:'+(end-start)+' Milisegundos <br>'
    $('#resultado').append(resultado)
    console.log ('start:', start, 'end:', end, 'Diferencia:',end-start);
    });
