import grpc
import Branch_pb2
import Branch_pb2_grpc
import time
import sys
import json
import time

# main can be a loop that parses JSON input, assigns a PID to each Customer process and calls
# RPC Serve() which will have to be implemented. Here the server can send back the metadata
# as it responds that it is listening. Then the Customer process can connect using the stub
# and pass the events to the server using executeEvents. The Customer will write the returned
# response to a file.

# Still need to think through propogate method that MsgDelivery can route to. Also need to
# think about the Branch type input messages.


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
        server_port = 50050 + self.id
        print('The port number for Customer {0} is {1}'.format(
            self.id, server_port))
        # channel = grpc.insecure_channel(
        #    'localhost:{}'.format(server_port))
        #self.stub = Branch_pb2_grpc.BranchStub(channel)

    # TODO: students are expected to send out the events to the Bank
    def executeEvents(self):
        request = Branch_pb2.Request(
            id=self.id, type='customer', event=self.events)
        print(request)
        #response = Branch_pb2.MsgDelivery(request)
        # print(response)
        print('-' * 30)


def main():
    with open(sys.argv[1]) as f:
        invalid_json = f.read()

    mid_json = invalid_json.replace('“', '"').replace('”', '"')
    valid_json = json.loads(mid_json)

    for request in valid_json:
        for attribute, value in request.items():
            if value == "customer":
                C = Customer(request['id'], request['events'])
                C.createStub()
                C.executeEvents()
                time.sleep(1)


if __name__ == "__main__":
    main()
