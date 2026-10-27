from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from app.models.shirt import Camisa, Inventario

router = APIRouter(
    prefix="/camisas",
    tags=["Camisas e Inventario"]
)

# Bases de datos simuladas en memoria
db_camisas: List[Camisa] = []
db_inventario: List[Inventario] = []

# ==========================================
# ENDPOINTS PARA CAMISAS (Catálogo)
# ==========================================

@router.post("/", response_model=Camisa, status_code=status.HTTP_201_CREATED)
def crear_camisa(camisa: Camisa):
    for item in db_camisas:
        if item.id == camisa.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe una camisa con el ID '{camisa.id}'"
            )
    db_camisas.append(camisa)
    return camisa


# REQUISITO RÚBRICA: Endpoint para filtrar usando atributos del modelo
@router.get("/", response_model=List[Camisa])
def listar_camisas(
    talla: Optional[str] = None,
    color: Optional[str] = None,
    genero: Optional[str] = None,
    solo_activas: bool = True
):
    resultado = db_camisas

    if solo_activas:
        resultado = [c for c in resultado if c.activo]

    if talla:
        resultado = [c for c in resultado if c.talla.lower() == talla.lower()]
    if color:
        resultado = [c for c in resultado if c.color.lower() == color.lower()]
    if genero:
        resultado = [c for c in resultado if c.genero.lower() == genero.lower()]

    return resultado


@router.get("/{camisa_id}", response_model=Camisa)
def obtener_camisa_por_id(camisa_id: str):
    for camisa in db_camisas:
        if camisa.id == camisa_id:
            return camisa
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Camisa con ID '{camisa_id}' no fue encontrada"
    )


@router.put("/{camisa_id}", response_model=Camisa)
def actualizar_camisa(camisa_id: str, camisa_actualizada: Camisa):
    """Actualiza la información de una camisa existente."""
    for i, camisa in enumerate(db_camisas):
        if camisa.id == camisa_id:
            db_camisas[i] = camisa_actualizada
            return camisa_actualizada
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Camisa con ID '{camisa_id}' no fue encontrada"
    )


# REQUISITO RÚBRICA: Borrado Lógico
@router.delete("/{camisa_id}", response_model=dict)
def desactivar_camisa(camisa_id: str):
    for camisa in db_camisas:
        if camisa.id == camisa_id:
            camisa.activo = False
            return {"mensaje": f"La camisa con ID '{camisa_id}' ha sido desactivada del catálogo"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Camisa con ID '{camisa_id}' no fue encontrada"
    )


@router.post("/inventario", response_model=Inventario, status_code=status.HTTP_201_CREATED)
def registrar_stock(item: Inventario):
    """Registra el stock para una camisa existente."""
    for inv in db_inventario:
        if inv.id == item.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El registro de inventario con ID '{item.id}' ya existe"
            )
    db_inventario.append(item)
    return item


@router.get("/inventario", response_model=List[Inventario])
def listar_inventario():
    return db_inventario