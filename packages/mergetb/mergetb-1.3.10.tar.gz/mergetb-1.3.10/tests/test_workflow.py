import sys
from timeout_timer import timeout, TimeoutInterrupt 

# mergetb imports
import mergetb.mergetb as mergetb
from mergetb.identity import Identity
from mergetb.workspace import Experiment
from mergetb.realize import Realization
from mergetb.materialize import Materialization
from mergetb.types import StatusType
from mergetb.grpc_client import MergeGRPCError

# common test package imports
from .test_common import check_prompt_credentials

# Wait 15 seconds for a realization to complete
RLZ_TIMEOUT = 15

# Wait 60 seconds for a materialization to complete
MTZ_TIMEOUT = 60

exp = None
try:
    # Login to your account
    username, password = check_prompt_credentials()
    id = Identity(username, password)
    id.login()
    print("Logged in for user %s" % username)

    # Create experiment
    exp = Experiment("mergetbtest", username)
    exp.create()

    # Push a model and tag it v1
    exp.push_model("tests/data/model_test.py", tag="v1")

    # Realize tag v1
    rlz = Realization("v1", exp.name, exp.project, tag="v1")
    rlz.realize()

    # wait up to 10 seconds for the realization to succeed
    try:
        with timeout(RLZ_TIMEOUT):
            status = StatusType.Undefined 

            while True:
                resp = rlz.get()
                status = resp.status.highest_status

                if status == StatusType.Success:
                    print("realization succeeded")
                    break
                elif status == StatusType.Deleted:
                    raise Exception("realization deleted")
                elif status == StatusType.Pending:
                    print("realization pending")
                elif status == StatusType.Unresponsive:
                    raise Exception("realization unresponsive")
                elif status == StatusType.Processing:
                    print("realization processing")
                elif status == StatusType.Error:
                    raise Exception("realization error")
                else:
                    raise Exception("unknown realization error")
    except TimeoutInterrupt:
        raise Exception("realization did not succeed within %d seconds" % RLZ_TIMEOUT)

    resp = rlz.get()
    print("Realization expires at %s" % (resp.result.realization.expires))

    # set the rlz expiration time to 2 weeks from now
    rlz.update("2w")

    # get the new realization and check the expiration
    resp = rlz.get()
    print("Realization expires at %s" % (resp.result.realization.expires))

    # materialize it
    mtz = Materialization("v1", exp.name, exp.project)
    mtz.materialize()

    try:
        with timeout(MTZ_TIMEOUT):
            status = StatusType.Undefined 

            while True:
                resp = mtz.get()
                status = resp.status.highest_status

                if status == StatusType.Success:
                    print("materialization succeeded")
                    break
                elif status == StatusType.Deleted:
                    raise Exception("materialization deleted")
                elif status == StatusType.Pending:
                    print("materialization pending")
                elif status == StatusType.Unresponsive:
                    raise Exception("materialization unresponsive")
                elif status == StatusType.Processing:
                    print("materialization processing")
                elif status == StatusType.Error:
                    print("materialization error")
                    #raise Exception("materialization error")
                else:
                    raise Exception("unknown materialization error")
    except TimeoutInterrupt:
        raise Exception("materialization did not succeed within %d seconds" % MTZ_TIMEOUT)

# API errors are raised as MergeGRPCError
except MergeGRPCError as e:
    print(e)
except Exception as e:
    print(f"An unexpected error occurred: {e}")
else:
    print("test PASSED")
    sys.exit(0)
finally:
    # teardown the test
    if exp is not None:
        exp.delete()

print("test FAILED")
sys.exit(1)
