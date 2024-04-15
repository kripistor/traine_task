from typing import List
from uuid import UUID

from sqlalchemy import select

from app.models.user import User
from app.models.client import Client
from app.repo.repo import SQLAlchemyRepo
from app.schemas.client import ClientRead
from app.schemas.user import UserUpdate


class UserRepo(SQLAlchemyRepo):
    async def create_user(self, user: User) -> User:
        try:
            self.session.add(user)
            await self.session.commit()
            return user
        except Exception as e:
            await self.session.rollback()

    async def create_client(self, client: Client) -> Client:
        try:
            self.session.add(client)
            await self.session.commit()
            return client
        except Exception as e:
            await self.session.rollback()

    async def get_user_by_id(self, user_id: int) -> User:
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        user = result.scalars().first()
        return user

    async def get_user_by_login(self, login: str) -> User:
        stmt = select(User).where(User.login == login)
        result = await self.session.execute(stmt)
        user = result.scalars().first()
        return user

    async def get_client_by_id(self, client_id: int) -> Client:
        stmt = select(Client).where(Client.id == client_id)
        result = await self.session.execute(stmt)
        client = result.scalars().first()
        return client

    async def get_users_clients(self, user_id: int) -> List[ClientRead]:
        stmt = select(Client).where(Client.responsible_user_id == user_id)
        result = await self.session.execute(stmt)
        clients = result.scalars().all()
        return clients

    async def update_client_status(self, client_id: int, status: str) -> Client:
        client: Client = await self.get_client_by_id(client_id)
        setattr(client, "status", status)
        await self.session.commit()
        return client

    async def delete_clients(self, client_ids: List[int]):
        for client_id in client_ids:
            client: Client = await self.get_client_by_id(client_id)
            if client:
                await self.session.delete(client)
        await self.session.commit()
