from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from application.services.auth_service import authenticate_user, create_access_token
from infrastructure.databases.config.database import DBConfig as Database
from sqlalchemy.orm import Session

def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db: Session = Database.get_session("default")
    user = authenticate_user(form_data.username, form_data.password)
    db.close()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": str(user.id), "token_version": user.token_version}
    )
    return {"access_token": access_token, "token_type": "bearer"}
