import grpc
import Branch_pb2
import Branch_pb2_grpc
import time
import sys
import json


with open(sys.argv[1], 'r') as input_file:
    data = json.loads(input_file)


class Customer:
    def __init__(self, id, events):
        # unique ID of the Customer
        self.id = id
        # events from the input
        self.events = events
        # a list of received messages used for debugging purpose
        self.recvMsg = list()
        # pointer for the stub
        self.stub = None

    # TODO: students are expected to create the Customer stub

    def createStub(self):
        pass

    # TODO: students are expected to send out the events to the Bank
    def executeEvents(self):
        pass


class MsgDeliveryStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ClientRequest = channel.unary_unary(
            '/MsgDelivery/ClientRequest',
            request_serializer=Branch__pb2.Request.SerializeToString,
            response_deserializer=Branch__pb2.Response.FromString,
        )
