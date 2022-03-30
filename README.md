# gRPC Distributed Banking System

## Description

The gRPC Distributed Banking System demonstrates the use of Remote Procedure Calls in distributed systems. The banking model represented here is a shared account with several customers transacting on the same balance. Each customer completes their transaction with their own branch, and the branches are responsible for propagating balance changes to one another to maintain eventual consistency.

`Branch.proto` defines the interface through which Customers will communicate with the Branch. Request and Response types are composed from primitive types and a function is designated for handling the messages. Using gRPC, the pb2 files are generated to support the desired configuration.

`Branch.py` represents banking branches which are servers running on their own distinct ports, awaiting transaction requests. When a request for deposit or withdraw is received, the server handling the request will update its own balance and propagate the change to all other branches, who will then update their own balances. Then, the gRPC response is sent back to the Customer instance. If the request is a query, the shared balance is returned immediately.

`Customer.py` handles the input JSON file, and parses it to create multiprocessor Customer instances and their transactions. It configures a gRPC stub with the port of the waiting server, and then sends the customer requests to the appropriate branch. Once a response is received, it is placed in a multiprocessing queue until all workers have resolved their tasks, and the responses are formatted to an output file. If the transactions and propagations are handled successfully, the balance in the output file should match for every customer.

## To Run:

To run the program, use `python Customer.py __filename__` in Terminal, where the filename is your input file. An example input file 'input1.json' is provided with this project, and the example can be run with `python Customer.py input1.json `

The input file must be JSON. Smart quotes are not neccessary but are supported. The expected correct result for the example input file:

```
{'id': 1, 'recv': [{'interface': 'query', 'result': 'success', 'money': 500}]}
{'id': 2, 'recv': [{'interface': 'deposit', 'result': 'success'}, {'interface': 'query', 'result': 'success', 'money': 500}]}
{'id': 3, 'recv': [{'interface': 'withdraw', 'result': 'success'}, {'interface': 'query', 'result': 'success', 'money': 500}]}
```
