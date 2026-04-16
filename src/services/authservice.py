from datetime import timedelta, datetime
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError

from model.subjects import Account
from repositories.accrepo import AccRepository, get_acc_reposetory
from configs.settings import settings


security = HTTPBearer()


class AuthService:

    def __init__(
        self,
        repo: AccRepository,
        credentials: HTTPAuthorizationCredentials | None = None,
    ):
        self.repo = repo
        self.credentials = credentials
        self.pwd_context = CryptContext(schemes=["sha512_crypt"])

    def verify_password(self, password: str, hash_password: str):
        return self.pwd_context.verify(password, hash_password)

    async def autenticate_acc(
        self, email: str, password: str
    ) -> Account | bool:

        user = await self.repo.get_by_email(email)

        if not user:
            return False
        if not self.verify_password(password, user.password):
            return False

        return user

    def create_access_token(
        self, data: dict, exp_time: timedelta = None
    ) -> str:

        if exp_time:
            expire = datetime.utcnow() + exp_time

        else:
            expire = datetime.utcnow() + timedelta(minutes=15)

        data.update({"exp": expire})

        encodet_jwt = jwt.encode(
            data,
            key=settings.secret_key,
            algorithm=settings.algorithm,
            headers={"WWW-Autentihicate": "Bearer"},
        )

        return encodet_jwt

    async def get_curent_acc(self) -> Account:

        auth_exeption = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nor valid email or passwor",
        )

        try:
            payload = jwt.decode(
                self.credentials.credentials,
                settings.secret_key,
                algorithms=[settings.algorithm],
            )

            email = payload.get("sub")

            if not email:
                raise auth_exeption

            exp = payload.get("exp")

            # id exp ... TODO chek exp

        except JWTError:
            raise auth_exeption

        user = await self.repo.get_by_email(email)

        if not user:
            raise auth_exeption

        return user


async def get_reg_service(
    repo: AccRepository = Depends(get_acc_reposetory),
) -> AuthService:
    return AuthService(repo)


async def get_auth_service(
    repo: AccRepository = Depends(get_acc_reposetory),
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> AuthService:
    return AuthService(repo, credentials)
