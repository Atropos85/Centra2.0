import os
import sys
import django
import asyncio
import json
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path
import inspect

# ==== Configuración de entorno Django ====
sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/../../")))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "centra.settings")
django.setup()
load_dotenv()

# ==== Cliente OpenAI ====
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ==== Cargar funciones ====
from mpc_engine.services.function_map_cesantias import function_map
from mpc_engine.services.openai_tools import function_descriptions

# ==== Prompt de sistema desde archivo ====
def cargar_prompt(path_archivo: str) -> str:
    return Path(path_archivo).read_text(encoding="utf-8")

prompt_path = "mpc_engine/prompts/main.prompt"
system_message = {
    "role": "system",
    "content": cargar_prompt(prompt_path)
}

# ==== Lógica principal ====
async def main():
    messages = [system_message]
    print("🧠 Agente iniciado. Escribe tu mensaje ('salir' para terminar)\n")

    while True:
        user_input = input("Tú: ").strip()
        if user_input.lower() in ["salir", "exit", "quit"]:
            print("👋 Saliendo del agente.")
            break

        messages.append({"role": "user", "content": user_input})

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
                # Sigue el loop para procesar posibles respuestas encadenadas
                continue
            else:
                print("🤖 Agente:", message.content)
                messages.append({"role": "assistant", "content": message.content})
                break


if __name__ == "__main__":
    asyncio.run(main())
