from pydantic import BaseModel

class UsuarioBase(BaseModel):
    username: str
    colaborador_id: int
    rol_usuario_id: int

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioResponse(UsuarioBase):
    id: int
    is_active: bool
    created_at: str
    updated_at: str
    last_login: str | None
    token_version: int

    model_config = {"from_attributes": True}

class UsuarioPublic(BaseModel):
    id: int
    username: str
    colaborador_id: int
    rol_usuario_id: int
    is_active: bool
    token_version: int

    model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    sub: str | None = None
    token_version: int | None = None
