from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status

from repositories.accrepo import AccRepository, get_acc_reposetory
from schemas.accschemas import AccResponse, AccRegistrate


class AccService:
    def __init__(self, repo: AccRepository):
        self.repo = repo
        self.pwd_context = CryptContext(schemes=["sha512_crypt"])

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)


    async def get_user_by_email(self, email: str) -> AccResponse | None:

        post = await self.repo.get_by_email(email)
        return post

    async def create_user(self, user_data: AccRegistrate) -> AccResponse:
   
        if await self.get_user_by_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="user already exist",
            )

        data_dump = user_data.model_dump()
        data_dump["password"] = self.get_password_hash(
            data_dump["password"]
        )

        user = await self.repo.create(data_dump)

        return user


async def get_acc_service(
    repo: AccRepository = Depends(get_acc_reposetory),
) -> AccService:
    return AccService(repo)
