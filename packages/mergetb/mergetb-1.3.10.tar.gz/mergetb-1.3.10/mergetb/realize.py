import asyncio

from mergetbapi.portal.v1 import *
from .mergetb import do_grpc_call
from .grpc_client import MergeGRPCClient

class Realization(MergeGRPCClient):
    def __init__(self, name, experiment, project, revision=None, tag=None, branch=None,
                 duration=None, grpc_config=None, token=None):

        super().__init__(grpc_config, token)
        self.name = name
        self.experiment = experiment
        self.project = project
        self.revision = revision
        self.tag = tag
        self.branch = branch
        self.duration = duration

    async def _async_realize(self):
        return await RealizeStub(self.get_channel()).realize(
            RealizeRequest(
                project=self.project,
                experiment=self.experiment,
                realization=self.name,
                revision=self.revision,
                tag=self.tag,
                branch=self.branch,
                duration=self.duration,
            ), metadata=self.get_auth_metadata()
        )

    async def _async_get(self):
        return await RealizeStub(self.get_channel()).get_realization(
            GetRealizationRequest(
                project=self.project,
                experiment=self.experiment,
                realization=self.name,
                status_ms=-1,
            ), metadata=self.get_auth_metadata()
        )

    async def _async_update(self, duration=None):
        self.duration = duration

        return await RealizeStub(self.get_channel()).update_realization(
            UpdateRealizationRequest(
                project=self.project,
                experiment=self.experiment,
                realization=self.name,
                duration=ReservationDuration(
                    when=ReservationDurationCode.given,
                    duration=self.duration,
                )
            ), metadata=self.get_auth_metadata()
        )

    async def _async_relinquish(self):
        return await RealizeStub(self.get_channel()).relinquish(
            RelinquishRequest(
                project=self.project,
                experiment=self.experiment,
                realization=self.name,
            ), metadata=self.get_auth_metadata()
        )

    def realize(self):
        return do_grpc_call(self._async_realize)

    def get(self):
        return do_grpc_call(self._async_get)

    def update(self, duration=None):
        return do_grpc_call(self._async_update, duration)

    def relinquish(self):
        return do_grpc_call(self._async_relinquish)

    # SPHERE trappings; alias for realize/relinquish
    def reserve(self):
        return self.realize()

    def free(self):
        return self.relinquish()
