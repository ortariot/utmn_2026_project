from datetime import timedelta

from fastapi import APIRouter, Depends, status, HTTPException, Query

from schemas.accschemas import AccResponse, AccRegistrate
from schemas.authschemas import Token, Login
from services.accservice import AccService, get_acc_service
from services.authservice import AuthService, get_reg_service, get_auth_service
from configs.settings import settings

router = APIRouter()


@router.post("/registrate", response_model=AccResponse)
async def registrate(
    data: AccRegistrate, service: AccService = Depends(get_acc_service)
):
    res = await service.create_user(data)

    return res


@router.post("/token", response_model=Token)
async def login_of_access_token(
    from_data: Login, service: AuthService = Depends(get_reg_service)
):
    user = await service.autenticate_acc(from_data.email, from_data.password)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    access_token_exp = timedelta(minutes=settings.access_token_expire_minutes)

    access_token = service.create_access_token(
        {"sub": user.email}, access_token_exp
    )


    return  {"access_token": access_token, "token_type": "bearer" }


@router.get("/protected")
async def protect(service: AuthService = Depends(get_auth_service)):
    
    current_user = await service.get_curent_acc()


    return {"access": "ok"} 
