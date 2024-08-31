import asyncio

from mergetbapi.portal.v1 import *

from .mergetb import do_grpc_call
from .grpc_client import MergeGRPCClient

class XDC(MergeGRPCClient):
    def __init__(self, name, project, xdctype=XdcType.personal, channel=None, token=None):
        super().__init__(channel, token)
        self.name = name
        self.project = project
        self.xdctype = xdctype

    async def _async_create(self):
        return await XdcStub(self.get_channel()).create_xdc(
            CreateXdcRequest(
                project=self.project,
                xdc=self.name,
                type=self.xdctype,
            ), metadata=self.get_auth_metadata()
        )

    async def _async_get(self):
        return await XdcStub(self.get_channel()).get_xdc(
            GetXdcRequest(
                project=self.project,
                xdc=self.name,
                status_ms=-1,
            ), metadata=self.get_auth_metadata()
        )

    async def _async_delete(self):
        return await XdcStub(self.get_channel()).delete_xdc(
            DeleteXdcRequest(
                project=self.project,
                xdc=self.name,
            ), metadata=self.get_auth_metadata()
        )

    async def _async_attach(self, realization, experiment, project):
        return await XdcStub(self.get_channel()).attach_xdc(
            AttachXdcRequest(
                xdc=self.name,
                project=self.project,
                experiment=experiment,
                realization=realization,
                realization_project=project,
            ), metadata=self.get_auth_metadata()
        )

    async def _async_detach(self):
        return await XdcStub(self.get_channel()).detach_xdc(
            DetachXdcRequest(
                xdc=self.name,
                project=self.project,
            ), metadata=self.get_auth_metadata()
        )

    async def _async_detach(self):
        return await XdcStub(self.get_channel()).detach_xdc(
            DetachXdcRequest(
                xdc=self.name,
                project=self.project,
            ), metadata=self.get_auth_metadata()
        )

    def create(self):
        return do_grpc_call(self._async_create)

    def get(self):
        return do_grpc_call(self._async_get)

    def delete(self):
        return do_grpc_call(self._async_delete)

    def attach(self, realization, experiment, project):
        return do_grpc_call(self._async_attach, realization, experiment, project)

    def detach(self):
        return do_grpc_call(self._async_detach)
