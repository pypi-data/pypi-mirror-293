from mergetbapi.portal.v1 import *

from .grpc_client import MergeGRPCClient
from .mergetb import do_grpc_call

class Materialization(MergeGRPCClient):
    def __init__(self, name, experiment, project, channel=None, token=None):
        super().__init__(channel, token)
        self.name = name
        self.experiment = experiment
        self.project = project

    async def _async_materialize(self):
        return await MaterializeStub(self.get_channel()).materialize(
            MaterializeRequest(
                project=self.project,
                experiment=self.experiment,
                realization=self.name,
            ), metadata=self.get_auth_metadata()
        )

    async def _async_get(self):
        return await MaterializeStub(self.get_channel()).get_materialization_v2(
            GetMaterializationRequestV2(
                project=self.project,
                experiment=self.experiment,
                realization=self.name,
                status_ms=-1,
            ), metadata=self.get_auth_metadata()
        )

    async def _async_dematerialize(self):
        return await MaterializeStub(self.get_channel()).dematerialize(
            DematerializeRequest(
                project=self.project,
                experiment=self.experiment,
                realization=self.name,
            ), metadata=self.get_auth_metadata()
        )

    def materialize(self):
        return do_grpc_call(self._async_materialize)

    def get(self):
        return do_grpc_call(self._async_get)

    def dematerialize(self):
        return do_grpc_call(self._async_dematerialize)

    # SPHERE trappings - alias for materialize/dematerialize
    def activate(self):
        return self.materialize()

    def deactivate(self):
        return self.dematerialize()
