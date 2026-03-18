
from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from starlette.routing import Route
from app.models.usuario import UserBase
from app.data.database import users
from app.security.auth import verificar_Peticion


router= APIRouter (
    prefix= "/v1/users",
    tags= ["CRUD HTTP"]
    )


# -------------
# | ENDPOINTS |
# -------------

@router.get("/")
async def consultaUsuarios():
    return{
        "status":"200",
        "total": len(users),
        "data":users
        }
@router.post("/")
async def add_usuers(user:UserBase):
    for usr in users:
        if usr["id"] == user.id:
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
@router.put("/{id}") 
async def update_user(id: int, user_updated: dict):
    for index, usr in enumerate(users):
        if usr["id"] == id:
            user_updated["id"] = id 
            users[index] = user_updated
            return {
                "message": "Usuario actualizado correctamente",
                "datos": user_updated
            }
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado para actualizar"
    )

# ELIMINAR USUARIO (DELETE)
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: int, username:str= Depends(verificar_Peticion)):
    for index, usr in enumerate(users):
        if usr["id"] == id:
            users.pop(index) 
            return {
                "message": f"Usuario eliminado correctamente por {username}"
                }
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado para eliminar"
    )