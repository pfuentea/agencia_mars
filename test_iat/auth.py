from django.contrib import messages
from django.shortcuts import redirect, render
import bcrypt
from .models import User


def logout(request):
    if 'user' in request.session:
        del request.session['user']
    
    return redirect("/login")
    

def login(request):
    if request.method == "POST":
        print(request.POST)
        user = User.objects.filter(email=request.POST['email'])
        print(len(user))
        if user:
            log_user = user[0]

            if bcrypt.checkpw(request.POST['password'].encode(), log_user.password.encode()):
                #print(f"Log_user:{log_user.id}")
                user = {
                    "id" : log_user.id,
                    "name": f"{log_user.name}",
                    "email": log_user.email,
                    "role": log_user.role,
                }
                #print(f"User:{user}")
                request.session['user'] = user
                request.session['user_id'] = user.id
                request.session['from_login']="y"
                messages.success(request, "Logueado correctamente.")
                return redirect("/sitio_privado")
            else:
                messages.error(request, "Password o Email  incorrectos.")
        else:
            messages.error(request, "Email o password incorrectos.")



        return redirect("/login")
    else:
        return render(request, 'login.html')


def registro(request):
    if request.method == "POST":

        errors = User.objects.validador_basico(request.POST)
        # print(errors)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                # print("DESDE EL FOR: ",key, value)
            
            request.session['register_name'] =  request.POST['name']
            request.session['register_email'] =  request.POST['email']

        else:
            request.session['register_name'] = ""
            request.session['register_email'] = ""

            password_encryp = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode() 
            try:
                usuario_nuevo = User.objects.create(
                    name = request.POST['name'],
                    email=request.POST['email'],
                    password=password_encryp,
                    role=request.POST['role']
                )
                messages.success(request, "El usuario fue agregado con exito.")
            except:
                messages.warning(request, "El usuario ya existe.")
                return redirect("/login")

            

            request.session['user'] = {
                "id" : usuario_nuevo.id,
                "name": f"{usuario_nuevo.name}",
                "email": usuario_nuevo.email,
                "role": usuario_nuevo.role,
            }
            request.session['user_id'] = request.session['user']['id']
            return redirect("/sitio_privado")

        return redirect("/registro")
    else:
        return render(request, 'registro.html')
