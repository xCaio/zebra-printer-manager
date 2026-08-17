import re


def extract_fields(zpl_template: str) -> list[str]:
    fields = re.findall(r"{{(.*?)}}", zpl_template)
    return list(dict.fromkeys(fields))


def render_zpl(zpl_template: str, data: dict) -> str:
    fields = extract_fields(zpl_template)

    missing_fields = [
        field
        for field in fields
        if field not in data
    ]

    if missing_fields:
        raise ValueError(
            f"Campos obrigatórios ausentes: {missing_fields}"
        )

    rendered_zpl = zpl_template

    for field in fields:
        rendered_zpl = rendered_zpl.replace(
            f"{{{{{field}}}}}",
            str(data[field])
        )

    return rendered_zpl


def set_quantity(zpl: str, quantity: int) -> str:
    pattern = r"\^PQ\d+"

    if not re.search(pattern, zpl):
        raise ValueError(
            "Comando ^PQ não encontrado no ZPL"
        )

    return re.sub(
        pattern,
        f"^PQ{quantity}",
        zpl,
        count=1
    )