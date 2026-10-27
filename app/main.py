from fastapi import FastAPI
from app.routers import users_router, shirt_router, sale_router

app = FastAPI(title="API Tienda de Ropa")

app.include_router(users_router.router)
app.include_router(shirt_router.router)
app.include_router(sale_router.router)