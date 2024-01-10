# Consulting an API at https://jsonplaceholder.typicode.com/

import requests
from pprint import pprint

# GET - Get all resources
result_get = requests.get('https://jsonplaceholder.typicode.com/todos')
pprint(result_get.json())

# GET with ID - Retrieve a unique resource with id=2
result_get_with_id = requests.get(
    'https://jsonplaceholder.typicode.com/todos/2')
pprint(result_get_with_id.json())

# POST - Create a new resource
new_task = {
    'completed': False,
    'title': 'Wash the car',
    'userId': 1
}
result_post = requests.post(
    'https://jsonplaceholder.typicode.com/todos', new_task)
pprint(result_post.json())

# PUT - Modify an existing resource
modified_task = {
    'completed': False,
    'title': 'Wash the motorcycle',
    'userId': 1
}

result_put = requests.put(
    'https://jsonplaceholder.typicode.com/todos/2', modified_task)
pprint(result_put.json())

# DELETE - In this case, it will delete ID 2
result_delete = requests.delete('https://jsonplaceholder.typicode.com/todos/2')
pprint(result_delete.json())
