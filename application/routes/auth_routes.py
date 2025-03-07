from fastapi import APIRouter
from application.controllers.auth_controller import login

router = APIRouter(prefix="/auth", tags=["Authentication"])

router.post("/token")(login)
