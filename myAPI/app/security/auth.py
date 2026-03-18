
from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

# Seguridad con HTTP Basic

security = HTTPBasic()

def verificar_Peticion(credentials: HTTPBasicCredentials=Depends(security)):
    usuarioAuth= secrets.compare_digest(credentials.username,"iand")
    contraAuth= secrets.compare_digest(credentials.password,"1234")

    if not (usuarioAuth and contraAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
        )

    return credentials.username
