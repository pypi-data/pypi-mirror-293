from mergetbapi.portal.v1 import *

from .grpc_client import MergeGRPCClient
from .mergetb import do_grpc_call

class Cred(MergeGRPCClient):
    def __init__(self, username, channel=None, token=None):
        super().__init__(channel, token)
        self.username = username

    async def _async_get_user_ssh_keys(self):
        return await CredStub(self.get_channel()).get_user_ssh_keys(
            GetUserSshKeysRequest(username=self.username),
            metadata=self.get_auth_metadata(),
        )

    async def _async_get_user_ssh_cert(self):
        return await CredStub(self.get_channel()).get_user_ssh_cert(
            GetUserSshCertRequest(username=self.username),
            metadata=self.get_auth_metadata(),
        )

    def get_user_ssh_keys(self):
        return do_grpc_call(self._async_get_user_ssh_keys)

    def get_user_ssh_cert(self):
        return do_grpc_call(self._async_get_user_ssh_cert)
