from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from ..forms.login_forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import asyncio
import json
from mpc_engine.agent.handler import handle_message


@login_required
def home(request):
    print(f"User authenticated: {request.user.is_authenticated}")  # Debería ser True
    
    if request.user.is_authenticated:
        return render(request, "registration/base.html")
    else:
        return redirect('login') 

@csrf_exempt
def agent_chat(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "")
        chat_history = data.get("history", [])
        response_text, new_history = asyncio.run(handle_message(user_message, chat_history))
        return JsonResponse({"response": response_text, "history": new_history})
    return JsonResponse({"error": "Método no permitido"}, status=405)    

def redirect_to_login(request):
    return redirect('login')  # Redirige a la vista de inicio de sesión


def cust_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)  # Asegúrate de pasar los datos del POST
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # Inicia sesión al usuario
                return redirect('home')  # Redirige a la vista de índice
            else:
                return render(request, 'registration/login.html', {
                    'form': form,
                    'error': 'Invalid credentials'
                })
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

def cust_logout(request):

    print(f"User authenticated logout: {request.user.is_authenticated}")  # Debería ser True
    logout(request)  # Cierra la sesión
    print(f"User authenticated logout: {request.user.is_authenticated}")  # Debería ser True

    return redirect('login')  # Redirige a la página de inicio de sesión
