from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    id: int
    nombre: str
    apellido: str
    documento: str
    telefono: str
    email: EmailStr
    activo: bool = True

class Cliente(UserBase):
    direccion_envio: str
    tipo_de_cliente: str
    comprador: bool = True

class Vendedor(UserBase):
    cargo: str
    fecha_de_ingreso: str