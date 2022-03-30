import grpc
import Branch_pb2
import Branch_pb2_grpc
import time
import sys
import json
import multiprocessing
from google.protobuf.json_format import MessageToDict
import Branch


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

    def createStub(self, port, q):
        channel = grpc.insecure_channel(
            'localhost:{}'.format(port))
        stub = Branch_pb2_grpc.BranchStub(channel)
        self.stub = stub
        self.executeEvents(q)

    # stagger events to avoid race condition, place result in queue
    def executeEvents(self, q):
        eventid, eventiface, money = self.events['id'], self.events['interface'], self.events['money']
        if eventiface == 'query':
            time.sleep(1)
        elif eventiface == 'withdraw':
            time.sleep(.5)
        request = Branch_pb2.Request(
            id=self.id, type='customer', eventid=eventid, eventiface=eventiface, money=money)
        response = self.stub.MsgDelivery(request)
        result = MessageToDict(response)
        q.put(result)


def create_customer(port, cid, events, q):
    C = Customer(cid, events)
    C.createStub(port, q)


def output(q):
    clipboard = []
    wanted_keys = ['interface', 'result', 'money']

    while not q.empty():
        clipboard.append(q.get())

    for k in range(1, len(clipboard)):
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
    # taking input file, converting smart quotes
    with open(sys.argv[1]) as f:
        invalid_json = f.read()
    mid_json = invalid_json.replace('“', '"').replace('”', '"')
    valid_json = json.loads(mid_json)

    # build a list of branch IDs
    branches = []
    for request in valid_json:
        for attribute, value in request.items():
            if value == "branch":
                branches.append(request['id'])

    # create Branch processes, send to server function
    for request in valid_json:
        for attribute, value in request.items():
            if value == "branch":
                bid, balance, branchlist = request['id'], request['balance'], branches
                port = 50050 + bid
                worker = multiprocessing.Process(
                    target=Branch.serve, args=(port, bid, balance, branchlist))
                worker.start()

    # create Customer processes, send to create_customer function
    time.sleep(.25)
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
                        target=create_customer, args=(port, cid, events, q))
                    workers.append(worker)
                    worker.start()
    for worker in workers:
        worker.join()

    # call output after all workers are done
    output(q)
