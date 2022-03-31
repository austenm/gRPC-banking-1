import grpc
import generated.Branch_pb2 as Branch_pb2
import generated.Branch_pb2_grpc as Branch_pb2_grpc
from concurrent import futures


class Branch(Branch_pb2_grpc.BranchServicer):

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

    def MsgDelivery(self, request, context):
        amount = request.money
        request_type = request.type
        transaction_type = request.eventiface

        if request.eventiface == 'deposit' or request.eventiface == 'withdraw':
            self.balance = self.adjust_balance(
                amount, request_type, transaction_type)
            return Branch_pb2.Response(id=request.id, interface=transaction_type, result="success")
        else:
            return Branch_pb2.Response(id=request.id, interface="query", result="success", money=self.balance)

    def adjust_balance(self, amount, req_type, trans_type):
        if trans_type == 'deposit':
            new_bal = self.balance + amount
        else:
            new_bal = self.balance - amount
        if req_type == 'customer':
            self.propagate(amount, trans_type)
        return new_bal

    def propagate(self, amount, trans_type):
        for i in self.branches:
            if i != self.id:
                port = 50050 + i
                channel = grpc.insecure_channel(
                    'localhost:{}'.format(port))
                stub = Branch_pb2_grpc.BranchStub(channel)
                request = Branch_pb2.Request(
                    id=i, type='branch', eventid=0, eventiface=trans_type, money=amount)
                response = stub.MsgDelivery(request)


def serve(port, bid, balance, branches):
    B = Branch(bid, balance, branches)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Branch_pb2_grpc.add_BranchServicer_to_server(B, server)
    server.add_insecure_port('localhost:{}'.format(port))
    server.start()
    server.wait_for_termination(timeout=10)
