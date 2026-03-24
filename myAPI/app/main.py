# -----------------
# | IMPORTACIONES |
# -----------------

from fastapi import FastAPI
from app.routers import misc, users
from app.data.db import engine
from app.data import usuario

usuario.Base.metadata.create_all(bind=engine)

# --------------------------------------
# | INICIALIZAR LA INSTANCIA DE LA API |
# --------------------------------------

app = FastAPI(
    title = "My first API", 
    description = "Rodriguez Ruiz Ian David", 
    version = "1.0"
)

app.include_router(users.router)
app.include_router(misc.router)



