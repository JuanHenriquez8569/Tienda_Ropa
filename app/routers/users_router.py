from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.users import Cliente, Vendedor

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios (Clientes y Vendedores)"]
)

db_clientes: List[Cliente] = []
db_vendedores: List[Vendedor] = []

@router.post("/clientes", response_model=Cliente, status_code=status.HTTP_201_CREATED)
def crear_cliente(cliente: Cliente):
    for item in db_clientes:
        if item.id == cliente.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un cliente con el ID {cliente.id}"
            )
    db_clientes.append(cliente)
    return cliente


@router.get("/clientes", response_model=List[Cliente])
def listar_clientes():
    return db_clientes


@router.get("/clientes/buscar/documento/{doc}", response_model=Cliente)
def buscar_cliente_por_documento(doc: str):
    for cliente in db_clientes:
        if cliente.documento == doc:
            return cliente
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No se encontró ningún cliente con el documento {doc}"
    )


@router.get("/clientes/{cliente_id}", response_model=Cliente)
def obtener_cliente_por_id(cliente_id: int):
    for cliente in db_clientes:
        if cliente.id == cliente_id:
            return cliente
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Cliente con ID {cliente_id} no fue encontrado"
    )


@router.post("/vendedores", response_model=Vendedor, status_code=status.HTTP_201_CREATED)
def crear_vendedor(vendedor: Vendedor):
    for item in db_vendedores:
        if item.id == vendedor.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un vendedor registrado con el ID {vendedor.id}"
            )
    db_vendedores.append(vendedor)
    return vendedor


@router.get("/vendedores", response_model=List[Vendedor])
def listar_vendedores(solo_activos: bool = True):
    if solo_activos:
        return [v for v in db_vendedores if v.activo]
    return db_vendedores


@router.get("/vendedores/{vendedor_id}", response_model=Vendedor)
def obtener_vendedor_por_id(vendedor_id: int):
    for vendedor in db_vendedores:
        if vendedor.id == vendedor_id:
            return vendedor
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Vendedor con ID {vendedor_id} no fue encontrado"
    )


@router.delete("/vendedores/{vendedor_id}", response_model=dict)
def deshabilitar_vendedor(vendedor_id: int):
    for vendedor in db_vendedores:
        if vendedor.id == vendedor_id:
            vendedor.activo = False
            return {"mensaje": f"El vendedor '{vendedor.nombre} {vendedor.apellido}' ha sido desactivado"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Vendedor con ID {vendedor_id} no fue encontrado"
    )