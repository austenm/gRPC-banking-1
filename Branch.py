import grpc
import Branch_pb2
import Branch_pb2_grpc


class Branch(example_pb2_grpc.RPCServicer):

    def __init__(self, id, balance, branches):
        # unique ID of the Branch
        self.id = id
        # replica of the Branch's balance
        self.balance = balance
        # the list of process IDs of the branches
        self.branches = branches
        # the list of Client stubs to communicate with the branches
        self.stubList = list()
        # a list of received messages used for debugging purpose
        self.recvMsg = list()
        # iterate the processID of the branches

        # TODO: students are expected to store the processID of the branches
        pass

    # TODO: students are expected to process requests from both Client and Branch
    def MsgDelivery(self, request, context):
        pass


class MsgDeliveryServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ClientRequest(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MsgDeliveryServicer_to_server(servicer, server):
    rpc_method_handlers = {
        'ClientRequest': grpc.unary_unary_rpc_method_handler(
            servicer.ClientRequest,
            request_deserializer=Branch__pb2.Request.FromString,
            response_serializer=Branch__pb2.Response.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        'MsgDelivery', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
