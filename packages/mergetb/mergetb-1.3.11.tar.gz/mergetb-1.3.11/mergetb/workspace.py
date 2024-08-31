import asyncio
import paramiko

from mergetbapi.portal.v1 import Experiment as ExperimentV1
from mergetbapi.portal.v1 import *

from .mergetb import do_grpc_call
from .grpc_client import MergeGRPCClient
from .identity import Identity
from .model import Model
from .realize import Realization
from .materialize import Materialization
from .xdc import XDC

"""
We make the User object a sub-class of Identity so that methods of the latter can be invoked
by objects of the former

While Merge makes a distinction between these types, most users of this library likely will not
"""
class User(Identity):
    def __init__(self, username, password=None, channel=None, token=None):
        super().__init__(username, password, channel, token)

    async def _async_activate(self):
        return await WorkspaceStub(self.get_channel()).activate_user(
            ActivateUserRequest(username=self.username),
            metadata=self.get_auth_metadata()
        )

    async def _async_freeze(self):
        return await WorkspaceStub(self.get_channel()).freeze_user(
            FreezeUserRequest(username=self.username),
            metadata=self.get_auth_metadata()
        )

    async def _async_init(self):
        return await WorkspaceStub(self.get_channel()).init_user(
            InitUserRequest(username=self.username),
            metadata=self.get_auth_metadata()
        )

    async def _async_get(self):
        return await WorkspaceStub(self.get_channel()).get_user(
            GetUserRequest(
                username=self.username,
                status_ms=-1,
            ),
            metadata=self.get_auth_metadata()
        )

    async def _async_update(self, name=None, state=None, access_mode=None,
            organizations=None, projects=None, facilities=None, experiments=None,
            toggle_admin=False, institution=None, category=None, country=None,
            email=None, usstate=None):
        return await WorkspaceStub(self.get_channel()).update_user(
            UpdateUserRequest(
                username=self.username,
                name=name,
                state=state,
                access_mode=access_mode,
                organizations=organizations,
                projects=projects,
                facilities=facilities,
                experiments=experiments,
                toggle_admin=toggle_admin,
                institution=institution,
                category=category,
                country=country,
                email=email,
                usstate=usstate,
            ),
            metadata=self.get_auth_metadata()
        )

    async def _async_delete(self):
        return await WorkspaceStub(self.get_channel()).delete_user(
            DeleteUserRequest(user=self.username),
            metadata=self.get_auth_metadata()
        )

    async def _async_get_public_keys(self):
        return await WorkspaceStub(self.get_channel()).get_user_public_keys(
            GetUserPublicKeysRequest(user=self.username),
            metadata=self.get_auth_metadata()
        )

    async def _async_delete_public_keys(self):
        return await WorkspaceStub(self.get_channel()).delete_user_public_keys(
            DeleteUserPublicKeysRequest(user=self.username),
            metadata=self.get_auth_metadata()
        )

    async def _async_add_public_key(self, key):
        return await WorkspaceStub(self.get_channel()).add_user_public_key(
            AddUserPublicKeyRequest(user=self.username, key=key),
            metadata=self.get_auth_metadata()
        )

    async def _async_delete_public_key(self, key):
        return await WorkspaceStub(self.get_channel()).delete_user_public_key(
            DeleteUserPublicKeyRequest(user=self.username, fingerprint=key),
            metadata=self.get_auth_metadata()
        )

    def activate(self):
        return do_grpc_call(self._async_activate)

    def freeze(self):
        return do_grpc_call(self._async_freeze)

    def init(self):
        return do_grpc_call(self._async_init)

    def get(self):
        return do_grpc_call(self._async_get)

    def update(self, name=None, state=None, access_mode=None, organizations=None,
               projects=None, facilities=None, experiments=None, toggle_admin=False,
               institution=None, category=None, country=None, email=None, usstate=None):
        return do_grpc_call(self._async_update,
            name, state, access_mode, organizations, projects, facilities,
            experiments, toggle_admin, institution, category, country, email,
            usstate
        )

    def delete(self):
        return do_grpc_call(self._async_delete)

    def get_public_keys(self):
        return do_grpc_call(self._async_get_public_keys)

    def delete_public_keys(self):
        return do_grpc_call(self._async_delete_public_keys)

    def add_public_key(self, key):
        return do_grpc_call(self._async_add_public_key, key)

    def delete_public_key(self, key):
        return do_grpc_call(self._async_delete_public_key, key)

class Project(MergeGRPCClient):
    def __init__(self, name, channel=None, token=None):
        super().__init__(channel, token)
        self.name = name

    async def _async_create(self, username):
        return await WorkspaceStub(self.get_channel()).create_project(
            CreateProjectRequest(
                user=username, # strange that the API requires this ...
                project=self.name,
            ),
            metadata=self.get_auth_metadata()
        )

    async def _async_get(self):
        return await WorkspaceStub(self.get_channel()).get_project(
            GetProjectRequest(
                name=self.name,
                status_ms=-1,
            ),
            metadata=self.get_auth_metadata()
        )

    async def _async_update(self, description=None, access_mode=None, members=None, organization=None):
        return await WorkspaceStub(self.get_channel()).update_project(
            UpdateProjectRequest(
                name=self.name,
                description=description,
                access_mode=access_mode,
                members=members,
                organization=organization,
            ),
            metadata=self.get_auth_metadata()
        )

    async def _async_delete(self):
        return await WorkspaceStub(self.get_channel()).delete_project(
            DeleteProjectRequest(
                name=self.name,
            ),
            metadata=self.get_auth_metadata()
        )

    async def _async_get_members(self):
        return await WorkspaceStub(self.get_channel()).get_project_members(
            GetProjectMembersRequest(
                name=self.name,
            ),
            metadata=self.get_auth_metadata()
        )

    async def _async_add_member(self, username, member):
        return await WorkspaceStub(self.get_channel()).add_project_member(
            AddProjectMemberRequest(
                project=self.name,
                username=username,
                member=member,
            ),
            metadata=self.get_auth_metadata()
        )

    async def _async_get_member(self, username):
        return await WorkspaceStub(self.get_channel()).get_project_member(
            GetProjectMemberRequest(
                project=self.name,
                member=username,
            ),
            metadata=self.get_auth_metadata()
        )

    async def _async_update_member(self, username, member):
        return await WorkspaceStub(self.get_channel()).update_project_member(
            UpdateProjectMemberRequest(
                project=self.name,
                username=username,
                member=member,
            ),
            metadata=self.get_auth_metadata()
        )

    async def _async_delete_member(self, username):
        return await WorkspaceStub(self.get_channel()).delete_project_member(
            GetProjectMemberRequest(
                project=self.name,
                member=username,
            ),
            metadata=self.get_auth_metadata()
        )

    async def _async_get_experiments(self):
        return await WorkspaceStub(self.get_channel()).get_project_experiments(
            GetProjectExperimentsRequest(
                project=self.name,
            ),
            metadata=self.get_auth_metadata()
        )

    def create(self, username):
        return do_grpc_call(self._async_create, username)

    def get(self):
        return do_grpc_call(self._async_get)

    def update(self, description=None, access_mode=None, members=None, organization=None):
        return do_grpc_call(self._async_update,
            description, access_mode, members, organization
        )

    def delete(self):
        return do_grpc_call(self._async_delete)

    def add_member(self, username, member):
        return do_grpc_call(self._async_add_member, username, member)

    def get_member(self, username):
        return do_grpc_call(self._async_get_member, username)

    def update_member(self, username, member):
        return do_grpc_call(self._async_update_member, username, member)

    def delete_member(self, username):
        return do_grpc_call(self._async_delete_member, username)

    def get_members(self):
        return do_grpc_call(self._async_get_members)

    def get_experiments(self):
        return do_grpc_call(self._async_get_experiments)

class Organization(MergeGRPCClient):
    def __init__(self, name, channel=None, token=None):
        super().__init__(channel, token)
        self.name = name

    async def _async_create(self, username):
        return await WorkspaceStub(self.get_channel()).create_organization(
            CreateOrganizationRequest(
                user=username, # strange that the API requires this ...
                organization=self.name,
            ),
            metadata=self.get_auth_metadata()
        )

    async def _async_get(self):
        return await WorkspaceStub(self.get_channel()).get_organization(
            GetOrganizationRequest(
                name=self.name,
                status_ms=-1,
            ),
            metadata=self.get_auth_metadata()
        )

    async def _async_update(self, description=None, state=None, access_mode=None, members=None, projects=None):
        return await WorkspaceStub(self.get_channel()).update_organization(
            UpdateOrganizationRequest(
                name=self.name,
                description=description,
                state=state,
                access_mode=access_mode,
                members=members,
                projects=projects,
            ),
            metadata=self.get_auth_metadata()
        )

    async def _async_delete(self):
        return await WorkspaceStub(self.get_channel()).delete_organization(
            DeleteOrganizationRequest(
                name=self.name,
            ),
            metadata=self.get_auth_metadata()
        )

    async def _async_activate(self):
        return await WorkspaceStub(self.get_channel()).activate_organization(
            ActivateOrganizationRequest(
                organization=self.name,
            ),
            metadata=self.get_auth_metadata()
        )

    async def _async_freeze(self):
        return await WorkspaceStub(self.get_channel()).freeze_organization(
            FreezeOrganizationRequest(
                organization=self.name,
            ),
            metadata=self.get_auth_metadata()
        )

    async def _async_request_membership(self, username, member):
        return await WorkspaceStub(self.get_channel()).request_organization_membership(
            RequestOrganizationMembershipRequest(
                organization=self.name,
                id=username,
                kind=MembershipType.UserMember,
                member=member,
            ),
            metadata=self.get_auth_metadata()
        )

    async def _async_confirm_membership(self, username):
        return await WorkspaceStub(self.get_channel()).confirm_organization_membership(
            ConfirmOrganizationMembershipRequest(
                organization=self.name,
                id=username,
                kind=MembershipType.UserMember,
            ),
            metadata=self.get_auth_metadata()
        )

    async def _async_get_member(self, username):
        return await WorkspaceStub(self.get_channel()).get_organization_member(
            GetOrganizationMemberRequest(
                organization=self.name,
                username=username,
            ),
            metadata=self.get_auth_metadata()
        )

    async def _async_update_member(self, username, member):
        return await WorkspaceStub(self.get_channel()).update_organization_member(
            UpdateOrganizationMemberRequest(
                organization=self.name,
                username=username,
                member=member,
            ),
            metadata=self.get_auth_metadata()
        )

    async def _async_delete_member(self, username):
        return await WorkspaceStub(self.get_channel()).delete_organization_member(
            DeleteOrganizationMemberRequest(
                organization=self.name,
                username=username,
            ),
            metadata=self.get_auth_metadata()
        )

    async def _async_get_members(self):
        return await WorkspaceStub(self.get_channel()).get_organization_members(
            GetOrganizationMembersRequest(
                organization=self.name,
            ),
            metadata=self.get_auth_metadata()
        )

    async def _async_get_project(self, project):
        return await WorkspaceStub(self.get_channel()).get_organization_project(
            GetOrganizationProjectRequest(
                organization=self.name,
                project=project,
            ),
            metadata=self.get_auth_metadata()
        )

    async def _async_get_projects(self):
        return await WorkspaceStub(self.get_channel()).get_organization_projects(
            GetOrganizationProjectsRequest(
                organization=self.name,
            ),
            metadata=self.get_auth_metadata()
        )

    def create(self, username):
        return do_grpc_call(self._async_create, username)

    def get(self):
        return do_grpc_call(self._async_get)

    def update(self, description=None, state=None, access_mode=None, members=None, projects=None):
        return do_grpc_call(self._async_update,
            description, state, access_mode, members, projects,
        )

    def delete(self):
        return do_grpc_call(self._async_delete)

    def activate(self):
        return do_grpc_call(self._async_activate)

    def freeze(self):
        return do_grpc_call(self._async_freeze)

    def request_membership(self, username, member):
        return do_grpc_call(self._async_request_membership, username, member)

    def confirm_membership(self, username):
        return do_grpc_call(self._async_confirm_membership, username)

    def get_member(self, username):
        return do_grpc_call(self._async_get_member, username)

    def update_member(self, username, member):
        return do_grpc_call(self._async_update_member, username, member)

    def delete_member(self, username):
        return do_grpc_call(self._async_delete_member, username)

    def get_members(self):
        return do_grpc_call(self._async_get_members)

    def get_project(self, project):
        return do_grpc_call(self._async_get_project, project)

    def get_projects(self):
        return do_grpc_call(self._async_get_projects)

class Experiment(MergeGRPCClient):
    def __init__(self, name, project, description=None, channel=None, token=None):
        super().__init__(channel, token)
        self.name = name
        self.project = project
        self.description = description

    async def _async_create(self):
        return await WorkspaceStub(self.get_channel()).create_experiment(
            CreateExperimentRequest(
                ExperimentV1(
                    name=self.name,
                    project=self.project,
                    description=self.description,
                )
            ),
            metadata=self.get_auth_metadata()
        )

    async def _async_get(self, with_models=None):
        return await WorkspaceStub(self.get_channel()).get_experiment(
            GetExperimentRequest(
                experiment=self.name,
                project=self.project,
                with_models=with_models,
                status_ms=-1,
            ),
            metadata=self.get_auth_metadata()
        )

    async def _async_update(self, description=None, access_mode=None, creator=None, maintainers=None):
        return await WorkspaceStub(self.get_channel()).update_experiment(
            UpdateExperimentRequest(
                name=self.name,
                project=self.project,
                description=description,
                access_mode=access_mode,
                creator=creator,
                maintainers=maintainers,
            ),
            metadata=self.get_auth_metadata()
        )

    async def _async_delete(self):
        return await WorkspaceStub(self.get_channel()).delete_experiment(
            DeleteExperimentRequest(
                project=self.project,
                experiment=self.name,
            ),
            metadata=self.get_auth_metadata()
        )

    async def _async_get_revision(self, revision=None, encoding=None):
        return await WorkspaceStub(self.get_channel()).get_revision(
            GetRevisionRequest(
                name=self.name,
                project=self.project,
                revision=revision,
                encoding=encoding,
            ),
            metadata=self.get_auth_metadata()
        )

    async def _async_push_model(self, modelpath, branch=None, tag=None):
        return await ModelStub(self.get_channel()).push(
            PushRequest(
                project=self.project,
                experiment=self.name,
                model=Model(modelpath).contents(),
                branch=branch,
                tag=tag,
            ),
            metadata=self.get_auth_metadata()
        )

    def create(self):
        return do_grpc_call(self._async_create)

    def get(self, with_models=None):
        return do_grpc_call(self._async_get, with_models)

    def update(self, description=None, access_mode=None, creator=None, maintainers=None):
        return do_grpc_call(self._async_update, description, access_mode, creator, maintainers)

    def delete(self):
        return do_grpc_call(self._async_delete)

    def get_revision(self, revision=None, encoding=None):
        return do_grpc_call(self._async_update, revision, encoding)

    def push_model(self, modelpath, branch=None, tag=None):
        return do_grpc_call(self._async_push_model, modelpath, branch, tag)

    def realize(self, realization, revision=None, tag=None, branch=None, duration=None):
        # call into the realize package to create an object and realize it
        return Realization(
            realization, self.name, self.project,
            revision=revision, tag=tag, branch=branch,
            channel=self.channel,
        ).realize()

    def relinquish(self, realization):
        # call into the realize package to relinquish
        return Realization(
            realization, self.name, self.project,
        ).relinquish()

    def materialize(self, realization):
        # call into the materialize package to create an object and materialize it
        return Materialization(
            realization, self.name, self.project,
            channel=self.channel,
        ).materialize()

    def dematerialize(self, realization):
        # call into the materialize package to dematerialize
        return Materialization(
            realization, self.name, self.project,
            channel=self.channel,
        ).dematerialize()

    # SPHERE trappings - alias for realize/relinquish
    def reserve(self, realization, revision=None, tag=None, branch=None, duration=None):
        return self.realize(realization, revision, tag, branch, duration)

    def free(self, realization):
        return self.relinquish(realization)

    # SPHERE trappings - alias for materialize/dematerialize
    def activate(self, realization):
        return self.materialize(realization)

    def deactivate(self, realization):
        return self.dematerialize(realization)

    def attach_xdc(self, realization, xdcname, xdcproject):
        # call into the XDC package to attach
        return XDC(
            xdcname, xdcproject,
            channel=self.channel,
        ).attach(realization, self.name, self.project)

    # Attach the experiment to xdc
    def detach_xdc(self, xdcname, xdcproject):
        # call into the XDC package to detach
        return XDC(
            xdcname, xdcproject,
            channel=self.channel,
        ).detach()

    # Execute command on node using SSH
    def exec_on_node(self, username, node, cmd):
        ssh_client = paramiko.SSHClient()
        private_key = paramiko.RSAKey.from_private_key_file("/home/"+username+"/.ssh/merge_key")
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(node, username=username, pkey=private_key)
        (stdin, stdout, stderr) = ssh_client.exec_command(cmd)
        lines = stdout.readlines()
        elines = stderr.readlines()
        ssh_client.close()
        return (lines, elines)
