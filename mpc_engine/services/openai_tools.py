# mpc_engine/services/openai_tools.py

function_descriptions = [
    {
        "type": "function",
        "function": {
            "name": "buscar_funcionario_por_cedula",
            "description": "Busca al funcionario por su cédula en la base de datos.",
            "parameters": {
                "type": "object",
                "properties": {
                    "cedula": { "type": "string" }
                },
                "required": ["cedula"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "ver_estado_solicitud",
            "description": "Consulta el estado de una solicitud de cesantías por cédula.",
            "parameters": {
                "type": "object",
                "properties": {
                    "cedula": { "type": "string" }
                },
                "required": ["cedula"]
            }
        }
    }
]
