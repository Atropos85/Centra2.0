from pathlib import Path

def build_system_prompt(base_url: str) -> dict:
    path = "mpc_engine/prompts/main.prompt"
    prompt_base = Path(path).read_text(encoding="utf-8")

    prompt_final = prompt_base.replace(
        "{{URL_CREAR}}", f"{base_url}/cesantias/solicitudes/create"
    ).replace(
        "{{URL_EDITAR_BASE}}", f"{base_url}/cesantias/solicitudes/edit/"
    )

    return {"role": "system", "content": prompt_final}
