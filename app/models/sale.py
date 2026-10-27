from pydantic import BaseModel
from datetime import datetime

class Venta(BaseModel):
    id: str
    fecha: datetime
    total: float
    comprador_id: int
    vendedor_id: int
    estado: str = "completada"