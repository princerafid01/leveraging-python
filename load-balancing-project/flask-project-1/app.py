from flask import Flask
import json
import os
from files.LinkedList import LinkedList

app  = Flask(__name__)

@app.route('/')
def home():
    return 'Hello world from container 1'

@app.route('/api/v1/insert/<number>')
def insert_into_linked_list(number):
    ll = LinkedList()
    number = int(number)

    # Opening JSON file
    jsonFile = open('files/linkedList.json')

    # returns JSON object
    jsonData = json.load(jsonFile)
    temp = {list : None}
    jsonData['list'].append(number)

    newLinkedList = {'list' : []}
    for index , l in enumerate(jsonData['list']):
        # Insert into Linekd List
        ll.insert(l)
        # Creating a dictionary for inserting into linkedList.json
        newLinkedList['list'].append(l)

    #  Make json file with json data
    with open('files/linkedList.json', 'w') as jsonFile:
        json.dump(newLinkedList, jsonFile)

    return f'Linkedlist is {ll}'


@app.route('/api/v1/get_all')
def get_all():
    # Opening JSON file
    jsonFile = open('files/linkedList.json')

    # returns JSON object
    jsonData = json.load(jsonFile)

    # returns all the data of linkedList.json
    return jsonData

@app.route('/api/v1/print')
def print():
    ll = LinkedList()

    # Opening JSON file
    json_file = open('files/linkedList.json')

    # returns JSON object
    json_data = json.load(json_file)

    #  creating linked list from json data
    result_json = list()
    for index , l in enumerate(json_data['list']):
        # Formatting linked list to json
        key = 'node_' + str(index+1)
        result_json.append({ key : l })

    #  Make json file with json data
    with open('files/result.json', 'w') as json_file:
        json.dump(result_json, json_file)

    return 'result.json file created.'



if __name__ == "__main__":
    app.run(host='0.0.0.0')