# -----------------
# | IMPORTACIONES |
# -----------------

from typing import Optional
from fastapi import FastAPI, status, HTTPException
import asyncio


# --------------------------------------
# | INICIALIZAR LA INSTANCIA DE LA API |
# --------------------------------------

app = FastAPI(
    title = "My first API", 
    description = "Rodriguez Ruiz Ian David", 
    version = "1.0"
)

users = [
    {"id": 1, "name": "Daniela Lisset Elizalde Ortiz", "age": 20, "aka": "The most beautiful girl ihesiml"}, 
    {"id": 2, "name": "Gabriela Martinez Cruz", "age": 22, "aka": "My loyal friend"}, 
    {"id": 3, "name": "Alan David Santiago de Vicente", "age": 21, "aka": "The BOMB"},
    {"id": 4, "name": "Rodriguez Ruiz Ian David", "age": 21, "aka": "The best"}
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

@app.get("/v1/users", tags=['CRUD usuarios'])
async def consultaUsuarios():
    return{
        "status":"200",
        "total": len(users),
        "data":users
        }
@app.post("/v1/users", tags=['CRUD usuarios'])
async def add_usuers(user:dict):
    for usr in users:
        if usr["id"] == user.get("id"):
            raise HTTPException(
                status_code=400,
                detail= "El id ya existe"
            )
    users.append(user)
    return{
        "message":"Usuario agregado correctamente",
        "datos":user,
        "status":"200"
    }

# ACTUALIZAR USUARIO (PUT)
@app.put("/v1/users/{id}", tags=['CRUD usuarios'])
async def update_user(id: int, user_updated: dict):
    for index, usr in enumerate(users):
        if usr["id"] == id:
            # Aseguramos que el ID del objeto coincida con el de la URL
            user_updated["id"] = id 
            # Reemplazamos el usuario en la lista
            users[index] = user_updated
            return {
                "message": "Usuario actualizado correctamente",
                "datos": user_updated
            }
    
    # Si termina el ciclo y no encontró nada:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado para actualizar"
    )

# ELIMINAR USUARIO (DELETE)
@app.delete("/v1/users/{id}", tags=['CRUD usuarios'], status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: int):
    for index, usr in enumerate(users):
        if usr["id"] == id:
            users.pop(index) # Elimina el elemento de la lista
            return # En 204 No Content no se suele retornar cuerpo (body)
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado para eliminar"
    )