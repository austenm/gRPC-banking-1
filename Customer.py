import grpc
import Branch_pb2
import Branch_pb2_grpc
import time
import sys
import json
import time
import multiprocessing
from google.protobuf.json_format import MessageToDict


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


def createStub(port, cid, events):
    C = Customer(cid, events)
    channel = grpc.insecure_channel(
        'localhost:{}'.format(port))
    stub = Branch_pb2_grpc.BranchStub(channel)
    C.stub = stub
    executeEvents(C)


def executeEvents(cust_obj):
    eventid, eventiface, money = cust_obj.events['id'], cust_obj.events['interface'], cust_obj.events['money']
    request = Branch_pb2.Request(
        id=cust_obj.id, type='customer', eventid=eventid, eventiface=eventiface, money=money)
    response = cust_obj.stub.MsgDelivery(request)
    result = MessageToDict(response)
    output(result)
    print('Customer {0} response: {1}'.format(cust_obj.id, result))
    print('-' * 50)


def output(result):
    responses = []
    responses.append(result)
    print('Hi, Output function here! The results are:\n')
    print(responses)


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        invalid_json = f.read()
    mid_json = invalid_json.replace('“', '"').replace('”', '"')
    valid_json = json.loads(mid_json)

    workers = []
    for request in valid_json:
        for attribute, value in request.items():
            if value == "customer":
                elist = request['events']
                for event in elist:
                    if event['interface'] == 'query':
                        time.sleep(3)
                    cid, events = request['id'], event
                    port = 50050 + cid
                    worker = multiprocessing.Process(
                        target=createStub, args=(port, cid, events))
                    workers.append(worker)
                    worker.start()
                for i in workers:
                    worker.join()
