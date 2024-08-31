import tempfile
import validators
from urllib.request import urlretrieve

from mergetbapi.portal.v1 import *

from .grpc_client import MergeGRPCClient
from .mergetb import do_grpc_call

class Model(MergeGRPCClient):
    def __init__(self, modelpath, channel=None, token=None):
        super().__init__(channel, token)
        self.model = modelpath

    async def _async_compile(self):
        return await ModelStub(self.get_channel()).compile(
            CompileRequest(model=self.contents()),
            metadata=self.get_auth_metadata()
        )
 
    def contents(self):
        if validators.url(self.model):
            with tempfile.NamedTemporaryFile() as tmp:
                urlretrieve(self.model, tmp.name)
                return open(tmp.name, 'r').read()
        else:
            return open(self.model, 'r').read()

    def compile(self):
        return do_grpc_call(self._async_compile)
