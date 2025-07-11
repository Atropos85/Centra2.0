# mpc_engine/agent/handler.py
import os
import sys
import django
import json
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path
import inspect
import asyncio
import markdown

# ==== Configuración de entorno Django ====
sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/../../../")))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "centra.settings")
django.setup()
load_dotenv()

# ==== Cliente OpenAI ====
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

from mpc_engine.services.function_map_cesantias import function_map
from mpc_engine.services.openai_tools import function_descriptions
from mpc_engine.services.prompt_builder import build_system_prompt

def cargar_prompt(path_archivo: str) -> str:
    return Path(path_archivo).read_text(encoding="utf-8")

def cargar_prompt_con_urls(path_archivo: str, url_base: str) -> str:
    prompt_base = Path(path_archivo).read_text(encoding="utf-8")
    return prompt_base

base_url = os.getenv("BASE_URL", "http://127.0.0.1:8000")

system_message = build_system_prompt(base_url)

# ==== Lógica del agente para web ====
async def handle_message(user_input: str, history: list) -> tuple:
    messages = [system_message] + history + [{"role": "user", "content": user_input}]

    while True:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            tools=function_descriptions,
            tool_choice="auto"
        )

        message = response.choices[0].message

        if message.tool_calls:
            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)
                function = function_map.get(function_name)

                if function:
                    if inspect.iscoroutinefunction(function):
                        result = await function(**arguments)
                    else:
                        result = function(**arguments)

                    messages.append({
                        "role": "function",
                        "name": function_name,
                        "content": str(result)
                    })
            continue
        else:
            messages.append({"role": "assistant", "content": message.content})
            response_html = markdown.markdown(message.content)
    
            return response_html, messages[1:] 