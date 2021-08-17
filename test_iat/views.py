from django.shortcuts import render, HttpResponse

def index(request):
    context = {
        'saludo': 'Hola'
    }
    return render(request, 'index.html', context)


def second(request, name):
    return HttpResponse('Hola ' + name)

