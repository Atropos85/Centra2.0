# cesantias/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from mpc_engine.agent.agent_interface import CesantiasAgent

import asyncio

agent = CesantiasAgent()

@csrf_exempt
def index(request):
    return render(request, "index.html")

@csrf_exempt
def chat_api(request):
    if request.method == "POST":
        user_input = request.POST.get("message")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(agent.procesar_input(user_input))
        return JsonResponse({"response": result})
