# -----------------
# | IMPORTACIONES |
# -----------------

from typing import Optional
from fastapi import FastAPI
import asyncio


# --------------------------------------
# | INICIALIZAR LA INSTANCIA DE LA API |
# --------------------------------------

app = FastAPI(
    title = "My first API", 
    description = "Isaac Abdiel Sanchez Lopez", 
    version = "1.0"
)

users = [
    {"id": 1, "name": "Daniela Lisset Elizalde Ortiz", "age": 20, "aka": "The most beautiful girl ihesiml"}, 
    {"id": 2, "name": "Gabriela Martinez Cruz", "age": 22, "aka": "My loyal friend"}, 
    {"id": 3, "name": "Alan David Santiago de Vicente", "age": 21, "aka": "The BOMB"}
]

# -------------
# | ENDPOINTS |
# -------------

# ENDPOINT RAIZ DE LA API (GET)
@app.get("/", tags = ["Start"])
async def helloworld():
    return {"message": "Hello world FastAPI"}

# ENDPOINT "mensaje_de_bienvenida" (GET)
@app.get("/v1/welcome_message", tags = ["Start"])
async def welcome_message():
    return {"message": "Welcome to your API REST"}

# ENDPOINT "calificaciones" (GET)
@app.get("/v1/grades", tags = ["Asynchrony"])
async def grades():
    await asyncio.sleep(5)
    return {"message": "Your grade in TAI is 10"}

# ENDPOINT "usuario" (GET CON PARAMETRO OBLIGATORIO)
@app.get("/v1/user/{id}", tags = ["Required_parameter"])
async def user(id:int):
    await asyncio.sleep(3)
    return {"user_found": id}

# ENDPOINT "usuario_opcional" (GET CON PARAMETRO OPCIONAL)
@app.get("/v1/user_optional/", tags = ["Optional_parameter"])
async def user_optional(id:Optional[int]=None):
    await asyncio.sleep(3)
    if id is not None:
        for user in users:
            if user["id"] == id:
                return {"user": user}
            return {"message": "Usuario no encontrado"}
    return {"message": "No se proporciono id"}