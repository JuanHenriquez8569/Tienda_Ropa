from pydantic import BaseModel

class Camisa(BaseModel):
    id: str
    nombre: str
    genero: str
    precio: float
    talla: str
    color: str
    activo: bool = True

class Inventario(BaseModel):
    id: str
    camisa_id: str
    cantidad: int
    activo: bool = True