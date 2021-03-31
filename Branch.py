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
        self.stubList = list()
        # a list of received messages used for debugging purpose
        self.recvMsg = list()
        # iterate the processID of the branches

    def MsgDelivery(self, request, context):
        amount = request.money
        rtype = request.type
        if request.eventiface == 'deposit':
            self.balance = self.deposit(amount, rtype)
            return Branch_pb2.Response(id=request.id, interface="deposit", result="success")
        elif request.eventiface == 'withdraw':
            self.balance = self.withdraw(amount, rtype)
            return Branch_pb2.Response(id=request.id, interface="withdraw", result="success")
        else:
            return Branch_pb2.Response(id=request.id, interface="query", result="success", money=self.balance)

    def deposit(self, amount, rtype):
        newbalance = self.balance + amount
        # only propagate if first request - type will be customer
        if rtype == 'customer':
            self.prop_dp(amount)
        return newbalance

    def withdraw(self, amount, rtype):
        newbalance = self.balance - amount
        # only propagate if first request - type will be customer
        if rtype == 'customer':
            self.prop_wd(amount)
        return newbalance

    def prop_dp(self, amount):
        for i in self.branches:
            if i != self.id:
                port = 50050 + i
                channel = grpc.insecure_channel(
                    'localhost:{}'.format(port))
                stub = Branch_pb2_grpc.BranchStub(channel)
                request = Branch_pb2.Request(
                    id=i, type='branch', eventid=0, eventiface="deposit", money=amount)
                response = stub.MsgDelivery(request)

    def prop_wd(self, amount):
        for i in self.branches:
            if i != self.id:
                port = 50050 + i
                channel = grpc.insecure_channel(
                    'localhost:{}'.format(port))
                stub = Branch_pb2_grpc.BranchStub(channel)
                request = Branch_pb2.Request(
                    id=i, type='branch', eventid=0, eventiface="withdraw", money=amount)
                response = stub.MsgDelivery(request)


def serve(port, bid, balance, branches):
    B = Branch(bid, balance, branches)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Branch_pb2_grpc.add_BranchServicer_to_server(B, server)
    server.add_insecure_port('localhost:{}'.format(port))
    server.start()
    server.wait_for_termination(timeout=10)
