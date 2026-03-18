
from fastapi import APIRouter
import asyncio
from typing import Optional
from app.data.database import users

router = APIRouter(tags=["Miscelanius"]) 


# ENDPOINT RAIZ DE LA API (GET)
@router.get("/")
async def helloworld():
    return {"message": "Hello world FastAPI"}

# ENDPOINT "mensaje_de_bienvenida" (GET)
@router.get("/v1/welcome_message")
async def welcome_message():
    return {"message": "Welcome to your API REST"}

# ENDPOINT "calificaciones" (GET)
@router.get("/v1/grades")
async def grades():
    await asyncio.sleep(5)
    return {"message": "Your grade in TAI is 10"}

# ENDPOINT "usuario" (GET CON PARAMETRO OBLIGATORIO)
@router.get("/v1/user/{id}")
async def user(id:int):
    await asyncio.sleep(3)
    return {"user_found": id}

# ENDPOINT "usuario_opcional" (GET CON PARAMETRO OPCIONAL)
@router.get("/v1/user_optional/")
async def user_optional(id:Optional[int]=None):
    await asyncio.sleep(3)
    if id is not None:
        for user in users:
            if user["id"] == id:
                return {"user": user}
            return {"message": "Usuario no encontrado"}
    return {"message": "No se proporciono id"}
