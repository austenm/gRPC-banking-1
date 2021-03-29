import grpc
import Branch_pb2
import Branch_pb2_grpc
from concurrent import futures
import sys
import json
import time
import multiprocessing


class Branch(Branch_pb2_grpc.BranchServicer):

    def __init__(self, id, balance, branches):
        # unique ID of the Branch
        self.id = id
        # replica of the Branch's balance
        self.balance = balance
        # the list of process IDs of the branches
        self.branches = branches
        # the list of Client stubs to communicate with the branches
        # use list of branch ids to generate stub for each entry in list
        # propogate will iterate over stublist and call MsgDelivery
        # use createStub code to add stubs to this list
        self.stubList = list()
        # a list of received messages used for debugging purpose
        self.recvMsg = list()
        # iterate the processID of the branches

        # TODO: students are expected to store the processID of the branches
        pass

    def deposit(self, amount):
        newbalance = self.balance + amount
        # prop_dp(amount)
        return newbalance

    def withdraw(self, amount):
        newbalance = self.balance - amount
        # prop_wd(amount)
        return newbalance

    def prop_dp(self, amount):
        # loop through branches, run withdraw on all processes whose
        # id != self.id
        pass

    def prop_wd(self, amount):
        # loop through branches, run withdraw on all processes whose
        # id != self.id
        pass

    def MsgDelivery(self, request, context):
        amount = request.money
        if request.eventiface == 'deposit':
            self.balance = self.deposit(amount)
            return Branch_pb2.Response(id=request.id, interface="deposit", result="success")
        elif request.eventiface == 'withdraw':
            self.balance = self.withdraw(amount)
            return Branch_pb2.Response(id=request.id, interface="withdraw", result="success")
        else:
            time.sleep(3)
            return Branch_pb2.Response(id=request.id, interface="query", result="success", money=self.balance)


def serve(port, bid, balance, branches):
    B = Branch(bid, balance, branches)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Branch_pb2_grpc.add_BranchServicer_to_server(B, server)
    server.add_insecure_port('localhost:{}'.format(port))
    server.start()
    print('Server listening at localhost:{}'.format(port))
    server.wait_for_termination()


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        invalid_json = f.read()
    mid_json = invalid_json.replace('“', '"').replace('”', '"')
    valid_json = json.loads(mid_json)

    branches = []
    for request in valid_json:
        for attribute, value in request.items():
            if value == "branch":
                branches.append(request['id'])

    workers = []
    for request in valid_json:
        for attribute, value in request.items():
            if value == "branch":
                bid, balance, branchlist = request['id'], request['balance'], branches
                port = 50050 + bid
                worker = multiprocessing.Process(
                    target=serve, args=(port, bid, balance, branchlist))
                workers.append(worker)
                worker.start()
