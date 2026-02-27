from typing import Optional, Literal
from fastapi import FastAPI, status, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

# --- AQUÍ SE MODIFICÓ EL NOMBRE ---
app = FastAPI(
    title='API de Biblioteca',
    description='Ian Rodriguez', 
    version='1.0'
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Faltan datos o el formato no es válido", "errores": exc.errors()}
    )

libros = []
prestamos = []

CURRENT_YEAR = datetime.now().year

class UsuarioBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=50, description="Nombre del usuario")
    correo: EmailStr = Field(..., description="Correo electrónico válido")

class LibroBase(BaseModel):
    id: int = Field(..., gt=0, description="Identificador del libro")
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre del libro")
    anio_publicacion: int = Field(..., gt=1450, le=CURRENT_YEAR, description="Año de publicación")
    paginas: int = Field(..., gt=1, description="Número de páginas")
    estado: Literal["disponible", "prestado"] = Field(default="disponible", description="Estado del libro")

class PrestamoBase(BaseModel):
    id_prestamo: int = Field(..., gt=0, description="Identificador del préstamo")
    id_libro: int = Field(..., gt=0, description="Identificador del libro a prestar")
    usuario: UsuarioBase

@app.get("/", tags=['Inicio'])
async def holamundo():
    return {"mensaje": "API de Biblioteca en FastAPI"}

@app.post("/v1/libros/", status_code=status.HTTP_201_CREATED, tags=['CRUD Libros'])
async def registrar_libro(libro: LibroBase):
    for lib in libros:
        if lib["id"] == libro.id:
            raise HTTPException(status_code=400, detail="El ID del libro ya existe")
    
    libros.append(libro.model_dump()) 
    
    return {
        "mensaje": "Libro registrado exitosamente",
        "datos": libro,
        "status": "201"
    }

@app.get("/v1/libros/disponibles", tags=['CRUD Libros'])
async def listar_disponibles():
    disponibles = [lib for lib in libros if lib["estado"] == "disponible"]
    return {
        "status": "200",
        "total": len(disponibles),
        "data": disponibles
    }

@app.get("/v1/libros/buscar", tags=['CRUD Libros'])
async def buscar_libro(nombre: str):
    encontrados = [lib for lib in libros if nombre.lower() in lib["nombre"].lower()]
    return {
        "status": "200",
        "total": len(encontrados),
        "data": encontrados
    }

@app.post("/v1/prestamos/", status_code=status.HTTP_201_CREATED, tags=['CRUD Prestamos'])
async def registrar_prestamo(prestamo: PrestamoBase):
    libro_encontrado = None
    for lib in libros:
        if lib["id"] == prestamo.id_libro:
            libro_encontrado = lib
            break
            
    if not libro_encontrado:
        raise HTTPException(status_code=400, detail="El libro no existe")
        
    if libro_encontrado["estado"] == "prestado":
        raise HTTPException(status_code=409, detail="El libro ya está prestado")

    for p in prestamos:
        if p["id_prestamo"] == prestamo.id_prestamo:
            raise HTTPException(status_code=400, detail="El ID del préstamo ya existe")

    nuevo_prestamo = prestamo.model_dump()
    nuevo_prestamo["estado_prestamo"] = "activo"
    prestamos.append(nuevo_prestamo)
    
    libro_encontrado["estado"] = "prestado"
    
    return {
        "mensaje": "Préstamo registrado",
        "datos": nuevo_prestamo,
        "status": "201"
    }

@app.put("/v1/prestamos/{id_prestamo}/devolver", status_code=status.HTTP_200_OK, tags=['CRUD Prestamos'])
async def devolver_libro(id_prestamo: int):
    for p in prestamos:
        if p["id_prestamo"] == id_prestamo:
            if p["estado_prestamo"] == "devuelto":
                raise HTTPException(status_code=409, detail="El libro ya fue devuelto anteriormente")
                
            p["estado_prestamo"] = "devuelto"
            for lib in libros:
                if lib["id"] == p["id_libro"]:
                    lib["estado"] = "disponible"
                    break
                    
            return {"mensaje": "Libro devuelto con éxito", "status": "200"}
            
    raise HTTPException(status_code=409, detail="El registro de préstamo activo no existe")

@app.delete("/v1/prestamos/{id_prestamo}", status_code=status.HTTP_200_OK, tags=['CRUD Prestamos'])
async def eliminar_prestamo(id_prestamo: int):
    for index, p in enumerate(prestamos):
        if p["id_prestamo"] == id_prestamo:
            if p["estado_prestamo"] == "activo":
                for lib in libros:
                    if lib["id"] == p["id_libro"]:
                        lib["estado"] = "disponible"
                        break
                        
            prestamos.pop(index)
            return {
                "mensaje": "Registro de préstamo eliminado",
                "id_eliminado": id_prestamo,
                "status": "200"
            }
            
    raise HTTPException(status_code=409, detail="El registro de préstamo ya no existe")