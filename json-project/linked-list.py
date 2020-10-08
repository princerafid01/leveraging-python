import json
from LinkedList import LinkedList

ll = LinkedList()

# Opening JSON file
json_file = open('linkedList.json')

# returns JSON object
json_data = json.load(json_file)

#  creating linked list from json data
result_json = list()
for index , l in enumerate(json_data['list']):
    ll.insert(l)
    # Formatting linked list to json
    key = 'node_' + str(index+1)
    result_json.append({ key : l })

print(f'Linkedlist is {ll}')

#  Make json file with json data
with open('result.json', 'w') as json_file:
  json.dump(result_json, json_file)

print('result.json file created.')



