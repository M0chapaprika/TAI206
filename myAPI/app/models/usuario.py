#Modelo de validacion Pydantic

from pydantic import BaseModel, Field

class UserBase(BaseModel):
    name:str = Field(..., min_length= 3, max_length= 50, description="Nombre del usuario")
    age:int = Field(..., ge= 0, le= 121, description="Edad validada entre 0 y 121"  )
    aka:str = Field(..., min_length= 3, max_length= 50, description="Alias del usuario", example="The best")   
