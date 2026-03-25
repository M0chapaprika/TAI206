from fastapi import status, HTTPException, Depends, APIRouter
from app.models.usuario import UserBase
from app.security.auth import verificar_Peticion

from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuario import Usuario as UsuarioDB

router = APIRouter(
    prefix="/v1/users",
    tags=["CRUD HTTP"]
)

# -------------
# | ENDPOINTS |
# -------------

# 1. OBTENER TODOS LOS USUARIOS (GET)
@router.get("/")
async def read_users(db: Session = Depends(get_db)):
    consultusers = db.query(UsuarioDB).all()
    return {
        "status": "200",
        "total": len(consultusers),
        "data": consultusers
    }

# 2. OBTENER USUARIO POR ID (GET)
@router.get("/{id}")
async def read_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(UsuarioDB).filter(UsuarioDB.id == id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con el id {id} no encontrado"
        )
        
    return {
        "status": "200",
        "data": user
    }

# 3. AGREGAR USUARIO (POST)
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

# 4. ACTUALIZAR USUARIO (PUT)
@router.put("/{id}") 
async def update_user(id: int, user_updated: UserBase, db: Session = Depends(get_db)):
    user = db.query(UsuarioDB).filter(UsuarioDB.id == id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado para actualizar"
        )
    
    user.name = user_updated.name
    user.age = user_updated.age
    user.aka = user_updated.aka
    
    db.commit()
    db.refresh(user)
    
    return {
        "message": "Usuario actualizado correctamente",
        "datos": user
    }

# 5. ACTUALIZAR USUARIO (PATCH)
@router.patch("/{id}")
async def patch_user(id: int, user_updated: dict, db: Session = Depends(get_db)):
    user = db.query(UsuarioDB).filter(UsuarioDB.id == id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado para parchear"
        )
    
    if "name" in user_updated:
        user.name = user_updated["name"]
    if "age" in user_updated:
        user.age = user_updated["age"]
    if "aka" in user_updated:
        user.aka = user_updated["aka"]

    db.commit()
    db.refresh(user)
    
    return {
        "message": "Usuario parcheado correctamente",
        "datos": user
    }

# 6. ELIMINAR USUARIO (DELETE)
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: int, db: Session = Depends(get_db), username: str = Depends(verificar_Peticion)):
    user = db.query(UsuarioDB).filter(UsuarioDB.id == id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado para eliminar"
        )
    
    db.delete(user)
    db.commit()
    
    return None