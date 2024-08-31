from grpclib.client import Channel
from google.rpc.error_details_pb2 import BadRequest

DEFAULT_PORTAL_URL = "grpc.sphere-testbed.net"
DEFAULT_PORTAL_PORT = 443
DEFAULT_PORTAL_SSL = True

class MergeGRPCConfig:
    def __init__(self, server, port=DEFAULT_PORTAL_PORT, ssl=DEFAULT_PORTAL_SSL):
        self.server = server
        self.port = port
        self.ssl = ssl

    def __str__(self):
        return "%s:%d (ssl=%d)" % (
            self.server, self.port, self.ssl
        )

dflt_grpc_config  = MergeGRPCConfig(DEFAULT_PORTAL_URL)
dflt_grpc_token   = None
dflt_grpc_channel = None

# initialize a GRPC channel
def _initialize_grpc_channel(grpc_config):
    return Channel(
        grpc_config.server,
        grpc_config.port,
        ssl=grpc_config.ssl,
    )

def set_grpc_config(config):
    global dflt_grpc_config
    dflt_grpc_config = config

class MergeGRPCClient:
    def __init__(self, channel=None, token=None):
        self.token = token
        self.channel = channel
        self.inited_channel = False

    def __str__(self):
        return self.token if self.token is not None else "(NULL)"

    def __del__(self):
        if self.inited_channel:
            self.channel.close()
            self.inited_channel = False

    def get_channel(self):
        if self.channel is  None:
            global dflt_grpc_config
            self.channel = _initialize_grpc_channel(dflt_grpc_config)
            self.inited_channel = True

        return self.channel

    def set_bearer_token(self, token):
        self.token = token

        # save in the default global token
        global dflt_grpc_token
        dflt_grpc_token = token

    def get_bearer_token(self):
        global dflt_grpc_token
        return self.token if self.token is not None else dflt_grpc_token

    def get_auth_metadata(self):
        return {
            "authorization": "Bearer %s" % self.get_bearer_token(),
        }

class MergeGRPCError(Exception):
    def __init__(self, grpc_error):
        self.grpc_error = grpc_error
        super().__init__(self.grpc_error.message)

    def __str__(self):
        # status: grpclib.const.Status
        # message: str
        # details: any
        if self.grpc_error.details is not None:
            for d in self.grpc_error.details:
                if isinstance(d, BadRequest):
                    return str(MergeError(d))

        return """
An Uncategorized MergeTB API Error Occurred:
    Message:     %s
    Status Code: %d (%s)
    Details:     %s""" % ( 
        self.grpc_error.message, 
        self.grpc_error.status.value, 
        self.grpc_error.status.name, 
        self.grpc_error.details
    )

    def __repr__(self):
        return self.__str__()

class MergeError():
    def __init__(self, badrequest):
        self.fields = {}
        for v in badrequest.field_violations:
            self.fields[v.field.lower()] = v.description

    def __str__(self):
        title = self.get_field('title')
        detail = self.get_field('detail')
        instance = self.get_field('instance')
        evidence = self.get_field('evidence')
        type = self.get_field('type')
        timestamp = self.get_field('timestamp')
        
        s = '\nA MergeTB API Error Occurred:'
        if title != '':
            s = s + '\n    Title:      %s' % title
        if detail != '':
            s = s + '\n    Detail:     %s' % detail
        if instance != '':
            s = s + '\n    Instance:   %s' % instance
        if evidence != '':
            s = s + '\n    Evidence:   %s' % evidence
        if type != '':
            s = s + '\n    Type:       %s' % type
        if timestamp != '':
            s = s + '\n    Timestamp:  %s' % timestamp

        return s

    def __repr__(self):
        return self.__str__()

    def get_field(self, field):
        return self.fields[field] if field in self.fields else ''
