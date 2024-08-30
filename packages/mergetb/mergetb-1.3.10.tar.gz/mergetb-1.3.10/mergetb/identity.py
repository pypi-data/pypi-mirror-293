import asyncio

from mergetbapi.portal.v1 import *

from .grpc_client import MergeGRPCClient
from .mergetb import do_grpc_call

class Identity(MergeGRPCClient):
    def __init__(self, username, password=None, channel=None, token=None):
        super().__init__(channel, token)
        self.username = username
        self.password = password

    async def _async_login(self):
        response = await IdentityStub(self.get_channel()).login(
            LoginRequest(username=self.username, password=self.password)
        )
        self.set_bearer_token(response.token)
        return response

    async def _async_logout(self):
        return await IdentityStub(self.get_channel()).logout(
            LogoutRequest(username=self.username),
            metadata=self.get_auth_metadata(),
        )

    async def _async_get(self):
        return await IdentityStub(self.get_channel()).get_identity(
            GetIdentityRequest(username=self.username),
            metadata=self.get_auth_metadata(),
        )

    async def _async_register(self, password, email, institution, category, country, usstate, name, admin=False):
        return await IdentityStub(self.get_channel()).register(RegisterRequest(
            username=self.username,
            email=email,
            password=password,
            institution=institution,
            category=category,
            country=country,
            usstate=usstate,
            name=name,
            admin=admin
        ))

    async def _async_unregister(self):
        return IdentityStub(self.get_channel()).register(UnregisterRequest(
            username=self.username,
            metadata=self.get_auth_metadata(),
        ))

    def login(self):
        return do_grpc_call(self._async_login)

    def logout(self):
        return do_grpc_call(self._async_logout)

    def get(self):
        return do_grpc_call(self._async_get)

    def register(self, password, email, institution, category, country, usstate, name, admin=False):
        return do_grpc_call(self._async_register,
            email, institution, category, country, usstate, name, admin
        )

    def unregister(self):
        return do_grpc_call(self._async_unregister)
