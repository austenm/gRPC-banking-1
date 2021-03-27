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

    def deposit(self, amount):
        newbalance = self.balance + amount
        return newbalance

    def withdraw(self, amount):
        newbalance = self.balance - amount
        return newbalance

    # def query(self):
    #    return self.balance

    # TODO: students are expected to process requests from both Client and Branch
    def MsgDelivery(self, request, context):
        for r in request:
            requester = r['type']
            if requester == 'customer':
                events = r['events']
                for event in events:
                    amount = event['money']
                    print(amount)
                    if event['interface'] == 'deposit':
                        self.balance = self.deposit(amount)
                    elif event['interface'] == 'withdraw':
                        self.balance = self.withdraw(amount)
                    else:
                        print('Good grief Charlie Brown.. just.. good GRIEF')
                    break
            elif requester == 'branch':
                print('This request type is: {}'.format(r['type']))
                print(r['balance'])


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Branch_pb2_grpc.add_MsgDeliveryServicer_to_server(
        Branch(), server)
    print('Starting server on port ')  # figure out which port
    server.add_insecure_port()  # figure out how to define your port here
    server.start()


def main():
    B = Branch(1, 400, 1)
    print('{0}, {1}, {2}'.format(B.id, B.balance, B.branches))
    request = [{'id': 1, 'type': 'customer', 'events': [
        {'id': 3, 'interface': 'query', 'money': 200}, {'id': 4, 'interface': 'deposit', 'money': 69000}]}, {'id': 1, 'type': 'branch', 'balance': 400}]
    context = 'whatever this is'
    B.MsgDelivery(request, context)
    print('{0}, {1}, {2}'.format(B.id, B.balance, B.branches))


if __name__ == "__main__":
    main()
