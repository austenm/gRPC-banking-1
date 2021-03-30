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


def createStub(port, cid, events, q):
    C = Customer(cid, events)
    channel = grpc.insecure_channel(
        'localhost:{}'.format(port))
    stub = Branch_pb2_grpc.BranchStub(channel)
    C.stub = stub
    executeEvents(C, q)


def executeEvents(cust_obj, q):
    eventid, eventiface, money = cust_obj.events['id'], cust_obj.events['interface'], cust_obj.events['money']
    request = Branch_pb2.Request(
        id=cust_obj.id, type='customer', eventid=eventid, eventiface=eventiface, money=money)
    response = cust_obj.stub.MsgDelivery(request)
    result = MessageToDict(response)
    q.put(result)
    # print('Customer {0} response: {1}'.format(cust_obj.id, result))
    # print('-' * 50)


def output(q):
    clipboard = []
    wanted_keys = ['interface', 'result', 'money']
    output_buf = []
    while not q.empty():
        clipboard.append(q.get())

    for k in range(11):
        newdict = {'id': k, 'recv': []}
        for i in clipboard:
            if i['id'] == k:
                clipdict = dict((key, i[key])
                                for key in wanted_keys if key in i)
                newdict['recv'].append(clipdict)
        if len(newdict['recv']):
            f = open("output.txt", "a")
            f.write('{}\n'.format(newdict))
            f.close()


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        invalid_json = f.read()
    mid_json = invalid_json.replace('“', '"').replace('”', '"')
    valid_json = json.loads(mid_json)

    q = multiprocessing.Queue()
    workers = []
    for request in valid_json:
        for attribute, value in request.items():
            if value == "customer":
                elist = request['events']
                for event in elist:
                    cid, events = request['id'], event
                    port = 50050 + cid
                    worker = multiprocessing.Process(
                        target=createStub, args=(port, cid, events, q))
                    workers.append(worker)
                    worker.start()
                for worker in workers:
                    worker.join()

    output(q)
    # while not q.empty():
    #     print('Contents of the Queue: {}'.format(q.get()))
