#Importaciones
from fastapi import FastAPI

#Inicializacion
app= FastAPI()

#Endpoints
@app.get("/")
async def holamundo():
    return {"mensaje":" Hola mundo FastAPI"}