import grpc
import example_pb2
import example_pb2_grpc
import time


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
