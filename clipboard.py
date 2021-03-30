file = [{'id': 1, 'interface': 'query', 'result': 'success', 'money': 400},
        {'id': 2, 'interface': 'deposit', 'result': 'success'},
        {'id': 2, 'interface': 'query', 'result': 'success', 'money': 570},
        {'id': 3, 'interface': 'withdraw', 'result': 'success'},
        {'id': 3, 'interface': 'query', 'result': 'success', 'money': 330}]


wanted_keys = ['interface', 'result', 'money']

# if 'id' == iter_num:
#   recv = []
#       ::that loop from down there::
#   dict = {'id': iter_num, 'recv': null}
#   dict['recv'] = recv


for k in range(11):
    newdict = {'id': k, 'recv': []}
    for i in file:
        if i['id'] == k:
            clipdict = dict((key, i[key]) for key in wanted_keys if key in i)
            newdict['recv'].append(clipdict)
    if len(newdict['recv']):
        print(newdict)
