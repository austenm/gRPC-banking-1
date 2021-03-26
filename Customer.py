import grpc
import Branch_pb2
import Branch_pb2_grpc
import time
import sys
import json

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

    def createStub(self, Customer):
        channel = grpc.insecure_channel(
            'localhost:{}'.format(5000 + Customer.id))
        stub = Branch_pb2_grpc.MsgDeliveryStub(channel)

    # TODO: students are expected to send out the events to the Bank
    def executeEvents(self, Customer):
        pass

    def printCustomerInfo(self):
        print(self.id)
        print(self.events)


def main():
    with open(sys.argv[1]) as f:
        invalid_json = f.read()

    mid_json = invalid_json.replace(
        'type', 'rtype').replace('“', '"').replace('”', '"')
    valid_json = json.loads(mid_json)

    for request in valid_json:
        for attribute, value in request.items():
            if value == "customer":
                C1 = Customer(request['id'], request['events'])
                C1.printCustomerInfo()


if __name__ == "__main__":
    main()


# prints both events from this object
# print(valid_json[1]['events'])

# prints the entire first event field of the first object
# print(valid_json[0]['events'][0])

# prints just the interface type (query in this example)
# print(valid_json[0]['events'][0]['interface'])
