import re


def extract_fields(zpl_template: str) -> list[str]:
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

    unknown_fields = [
        field for field in data
        if field not in fields
    ]

    if unknown_fields:
        raise ValueError(
            f"Campos não utilizados pelo layout: {unknown_fields}"
        )

    zpl = zpl_template

    for field, value in data.items():
        placeholder = f"{{{{{field}}}}}"
        zpl = zpl.replace(
            placeholder,
            str(value)
        )

    return zpl