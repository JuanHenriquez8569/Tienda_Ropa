from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from app.models.sale import Venta

router = APIRouter(
    prefix="/ventas",
    tags=["Ventas"]
)

db_ventas: List[Venta] = []


@router.post("/", response_model=Venta, status_code=status.HTTP_201_CREATED)
def registrar_venta(venta: Venta):
    for item in db_ventas:
        if item.id == venta.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"La venta con ID '{venta.id}' ya existe"
            )
    db_ventas.append(venta)
    return venta


@router.get("/", response_model=List[Venta])
def listar_ventas(estado: Optional[str] = None):
    if estado:
        return [v for v in db_ventas if v.estado.lower() == estado.lower()]
    return db_ventas


@router.get("/{venta_id}", response_model=Venta)
def obtener_venta_por_id(venta_id: str):
    for venta in db_ventas:
        if venta.id == venta_id:
            return venta
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Venta con ID '{venta_id}' no fue encontrada"
    )


# REQUISITO RÚBRICA: Borrado Lógico / Histórico en Transacciones
@router.delete("/{venta_id}", response_model=dict)
def anular_venta(venta_id: str):
    for venta in db_ventas:
        if venta.id == venta_id:
            venta.estado = "anulada"
            return {"mensaje": f"La venta '{venta_id}' ha sido anulada exitosamente (se conserva en el histórico)"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Venta con ID '{venta_id}' no fue encontrada"
    )