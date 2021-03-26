import grpc
import Branch_pb2
import Branch_pb2_grpc
from concurrent import futures


class Branch(Branch_pb2_grpc.MsgDeliveryServicer):

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
        message = MsgDelivery.Request(request)
        client_id = message.id
        request_type = message.type

    def deposit(self, amount):
        newbalance = Branch.balance + amount
        return newbalance

    def withdraw(self, amount):
        newbalance = Branch.balance - amount
        return newbalance

    def query(self):
        return Branch.balance


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Branch_pb2_grpc.add_MsgDeliveryServicer_to_server(Branch(), server)
    print('Starting server on port ')  # figure out which port
    server.add_insecure_port()  # figure out how to define your port here
    server.start()
