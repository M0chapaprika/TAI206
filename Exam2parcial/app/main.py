# -----------------
# | IMPORTACIONES |
# -----------------

from datetime import date, datetime
from fastapi import FastAPI, status, HTTPException, Depends
import asyncio
from typing import Optional
from fastapi import security
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

# --------------------------------------
# | INICIALIZAR LA INSTANCIA DE LA API |
# --------------------------------------

app = FastAPI(
    title = "Mi examen", 
    description = "Rodriguez Ruiz Ian David", 
    version = "1.0"
)

citas = [
    {"id": 1, "nombre": "Rodriguez Ruiz Ian David", "edad": 21, "fecha": "10/03/2026", "motivo": "Gripa" } 
]

#Modelo de validacion Pydantic
class UserBase(BaseModel):
    id:int = Field(..., gt= 0, description="Identificador de usuario", example=1)
    nombre:str = Field(..., min_length= 5, max_length= 50, description=" Nombre del paciente ")
    edad:int = Field(..., ge= 0, le= 121, description=" Edad validada entre 0 y 121 ") 
    fecha:date = Field(..., min_length= datetime, example=" Fecha actual ")
    motivo:str = Field(..., min_length= 0, max_length= 100, description=" Motivo de la cita ")


# Seguridad con HTTP Basic

security = HTTPBasic()

def verificar_Peticion(credentials: HTTPBasicCredentials=Depends(security)):
    usuarioAuth= secrets.compare_digest(credentials.username,"root")
    contraAuth= secrets.compare_digest(credentials.password,"1234")

    if not (usuarioAuth and contraAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
        )

    return credentials.username

# -------------
# | ENDPOINTS |
# -------------

# ENDPOINT RAIZ DE LA API (GET)
@app.get("/", tags = ["Start"])
async def helloworld():
    return {"message": "Hello world FastAPI"}

# ENDPOINT "usuario" (GET CON PARAMETRO OBLIGATORIO)
@app.get("/v1/cita/{id}", tags = ["Required_parameter"])
async def cita(id:int):
    await asyncio.sleep(3)
    return {"cita_found": id}

# ENDPOINT "usuario_opcional" (GET CON PARAMETRO OPCIONAL)
@app.get("/v1/cita_optional/", tags = ["Optional_parameter"])
async def cita_optional(id:Optional[int]=None):
    await asyncio.sleep(3)
    if id is not None:
        for cita in citas:
            if cita["id"] == id:
                return {"cita": cita}
            return {"message": " Cita no encontrada :("}
    return {"message": "No se proporciono id"}

@app.get("/v1/citas", tags=['CRUD citas'])
async def consultaCitas():
    return{
        "status":"200",
        "total": len(citas),
        "data":citas
        }
@app.post("/v1/citas", tags=['CRUD citas'])
async def add_citas(cita:UserBase):
    for cit in citas:
        if cit["id"] == cita.id:
            raise HTTPException(
                status_code=400,
                detail= "El id ya existe"
            )
    citas.append(cita)
    return{
        "message":"Usuario agregado correctamente",
        "datos":cita,
        "status":"200"
    }

# ACTUALIZAR USUARIO (PUT)
@app.put("/v1/citas/{id}", tags=['CRUD citas'])
async def update_cita(id: int, cita_updated: dict):
    for index, cit in enumerate(citas):
        if cit["id"] == id:
            cita_updated["id"] = id 
            citas[index] = cita_updated
            return {
                "message": " Cita actualizada correctamente ",
                "datos": cita_updated
            }
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=" Cita no encontrada para actualizar"
    )

# ELIMINAR USUARIO (DELETE)
@app.delete("/v1/citas/{id}", tags=['CRUD citas'], status_code=status.HTTP_204_NO_CONTENT)
async def delete_cita(id: int, username:str= Depends(verificar_Peticion)):
    for index, cit in enumerate(citas):
        if cit["id"] == id:
            citas.pop(index) 
            return {
                "message": f" Cita eliminada correctamente por {username}"
                }
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=" Cita no encontrada para eliminar "
    )