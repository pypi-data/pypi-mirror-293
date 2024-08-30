import sys

# mergetb imports
import mergetb.mergetb as mergetb
from mergetb.workspace import User
from mergetb.types import StatusType
from mergetb.grpc_client import MergeGRPCError

# common test package imports
from .test_common import check_prompt_credentials

try:
    # Login to your account via the User object 
    username, password = check_prompt_credentials()
    u = User(username, password)
    u.login()

    user = u.get().user
    summary="""User info for %s:
    Name:          %s
    State:         %s
    Access Mode:   %s
    Uid:           %d
    Gid:           %d
    Projects:      %s
    Experiments:   %s
    Organizations: %s
    Facilities:    %s
    Admin:         %d
    Institution:   %s
    Category:      %s
    Email:         %s
    Country:       %s
    US State:      %s""" % (
        username,
        user.name,
        user.state,
        user.access_mode,
        user.uid,
        user.gid,
        user.projects,
        user.experiments,
        user.organizations,
        user.facilities,
        user.admin,
        user.institution,
        user.category,
        user.email,
        user.country,
        user.usstate,
    )
    print(summary)

    projects = mergetb.get_projects().projects

    print()
    print("User has the following projects:")
    for project in projects:
        summary="""Project: %s
    Description:  %s
    Members:      %s
    Experiments:  %s
    Access Mode:  %d
    GID:          %d
    Organization: %s
    Category:     %s
    Subcategory:  %s""" % (
            project.name,
            project.description,
            project.members,
            project.experiments,
            project.access_mode,
            project.gid,
            project.organization,
            project.category,
            project.subcategory,
        )
        print(summary)

# API errors are raised as MergeGRPCError
except MergeGRPCError as e:
    print(e)
except Exception as e:
    print(f"An unexpected error occurred: {e}")
else:
    print("test PASSED")
    sys.exit(0)

print("test FAILED")
sys.exit(1)
