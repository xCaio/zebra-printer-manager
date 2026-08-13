import re

def extract_fields(zpl_template:str) -> list[str]:
    fields = re.findall(r"{{(.*?)}}", zpl_template)

    return list(dict.fromkeys(fields))

def render_zpl(zpl_template: str, data: dict) -> str:
    fields = extract_fields(zpl_template)

    missing_fields = [
        field for field in fields
        if field not in data
    ]

    if missing_fields:
        raise ValueError(
            f"Campos obrigatórios não informados: {missing_fields}"
        )

    zpl = zpl_template

    for field, value in data.items():
        placeholder = f"{{{{{field}}}}}"
        zpl = zpl.replace(placeholder, str(value))

    return zpl