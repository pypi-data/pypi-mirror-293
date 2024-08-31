import sys

# mergetb imports
from mergetb.identity import Identity
from mergetb.grpc_client import MergeGRPCError

# common test package imports
from .test_common import check_prompt_credentials

try:
    # Login to your account
    username, password = check_prompt_credentials()
    id = Identity(username, password)
    id.login()
    print("Logged in for user %s" % username)

    # Admin only
    resp = id.get().identity
    summary="""User info for %s:
    Email:  %s
    Admin:  %s
    Traits: %s""" % (
        username,
        resp.email,
        resp.admin,
        resp.traits,
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
