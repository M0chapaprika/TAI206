
from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from starlette.routing import Route
from app.models.usuario import UserBase
from app.data.database import users
from app.security.auth import verificar_Peticion

from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuario import Usuario as UsuarioDB


router= APIRouter (
    prefix= "/v1/users",
    tags= ["CRUD HTTP"]
    )


# -------------
# | ENDPOINTS |
# -------------

@router.get("/")
async def read_users(db:Session= Depends(get_db)):
    
    consultusers= db.query(UsuarioDB).all()
    
    return{
        "status":"200",
        "total": len(consultusers),
        "data":consultusers
        }
    
@router.post("/")
async def add_usuers(user: UserBase, db: Session = Depends(get_db)):

    newUser = UsuarioDB(name=user.name, age=user.age, aka=user.aka) 
    
    db.add(newUser)
    db.commit()
    db.refresh(newUser)

    return {
        "message": "Usuario agregado correctamente",
        "datos": newUser,
        "status": "200"
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
