from pydantic import BaseModel, Field
# {
#   "printer_id": 1,
#   "layout_id": 1,
#   "data": {
#     "codigo": "PPA000",
#     "nome_produto": "ETIQUETA TERMICA"
#   }
# }

class PrintRequest(BaseModel):
    printer_id: int = Field(gt=0)
    layout_id: int = Field(gt=0)
    quantity: int = Field(default=1, ge=1)
    data: dict[str, str | int | float | bool]


class PrintResponse(BaseModel):
    success: bool
    message: str
    printer: str
    layout: str