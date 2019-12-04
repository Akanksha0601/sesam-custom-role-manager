#!/usr/bin/env python3

import requests
import os
import json

jwt = os.environ.get('JWT')
node_api = os.environ.get('NODE_API')
node_subscription = os.environ.get('NODE_SUBSCRIPTION')
portal_api = os.environ.get('PORTAL_API')



# API urls
available_roles = portal_api + '/subscriptions/' + node_subscription + '/available-roles'
pipes_collection = node_api + '/permissions/pipes-collection'
pipe_permissions = node_api + '/permissions/pipes/'
pipes = node_api + '/pipes'
system_collection = node_api + '/permissions/systems-collection'
system_permissions = node_api + '/permissions/systems/'
systems = node_api + '/systems'

headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + jwt}


# print(available_roles )

# result = requests.get(url,params=None,headers=headers)

# print(result.content)

def create_role(role_name):
    url = available_roles
    print(role_name)
    print(url)
    payload = '{ "name": "' + role_name + '"}'

    print(payload)
    response = requests.request("POST", url, data=payload, headers=headers)
    return response


# pipe_roles##

def allow_create_pipe(role_id):
    url = pipes_collection
    payload = '[[\"allow\",[\"' + role_id + '\"],["add_pipe"]]]'
    response = requests.request("PUT", url, data=payload, headers=headers)
    return response


def set_pipe_permissions(role_id, pipe_id, permissions):
    url = pipe_permissions + pipe_id
    permissions = json.dumps(permissions)
    payload = "[[\"allow_all\",[\"" + role_id + "\"]," + permissions + "]]"
    print(payload)
    response = requests.request("PUT", url, data=payload, headers=headers)
    return response

# To cleanup local permissions from pipe
def remove_pipe_permissions(pipe_id):
    url = pipe_permissions + pipe_id
    payload = "[]"
    response = requests.request("PUT", url, data=payload, headers=headers)
    return response
##

def get_pipes():
    url = pipes
    response = requests.request("GET", url, headers=headers)
    return response

# system_roles##

def allow_create_system(role_id):
    url = system_collection
    payload = '[[\"allow\",[\"' + role_id + '\"],["add_system"]]]'
    response = requests.request("PUT", url, data=payload, headers=headers)
    return response


def set_system_permissions(role_id, system_id, permissions):
    url = system_permissions + system_id
    permissions = json.dumps(permissions)
    payload = "[[\"allow_all\",[\"" + role_id + "\"]," + permissions + "]]"
    print(payload)
    response = requests.request("PUT", url, data=payload, headers=headers)
    return response

# To cleanup local permissions from pipe

def remove_system_permissions(system_id):
    url = system_permissions + system_id
    payload = "[]"
    response = requests.request("PUT", url, data=payload, headers=headers)
    return response
##

def get_system():
    url = systems
    response = requests.request("GET", url, headers=headers)
    return response

def cleanup_permissions():
    for pipe in pipe_id_list:
        print(remove_pipe_permissions(pipe))
    for system in system_id_list:
        print(remove_system_permissions(system))


role_name = "AKSO-Admin"
json_response = json.loads(create_role(role_name).text)
print(json_response)
if json_response['status'] == 409:
    role_id = node_subscription + '_' + role_name
else:
    role_id = json_response['id']
print(role_id)
allow_create_pipe(role_id)
json_pipe_list = get_pipes().text
pipe_list = json.loads(json_pipe_list)

pipe_id_list = []

for pipe in pipe_list:
    pipe_id_list.append(pipe['_id'])

permissions_list = ["read_config", "write_config"]

for pipe in pipe_id_list:
    print(set_pipe_permissions(role_id, pipe, permissions_list))


print(allow_create_system(role_id))

json_system_list = get_system().text
system_list = json.loads(json_system_list)

system_id_list = []

for system in system_list:
    system_id_list.append(system['_id'])


for system in system_id_list:
    print(set_system_permissions(role_id, system, permissions_list))

#cleanup_permissions()
