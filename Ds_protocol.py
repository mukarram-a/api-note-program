'''

Creates JSON-formatted dictionaries to send to 'ds_client.py'.
JSON-formatted dictionaries allow the user to log on to the 
server, post messages, and edit their biography.

'''


# Mukarram A.
# Ds_protocol.py


import json
from profile import Post
from collections import namedtuple
post = Post()


DataTuple = namedtuple('DataTuple', ['foo','baz', 'barss'])

def extract_json(json_msg:str) -> DataTuple:
  '''
  Call the json.loads function on a json string and convert it to a DataTuple object
  
  '''
  try:
    json_obj = json.loads(json_msg)
    resp_message = json_obj['response']['message']
    resp_type = json_obj['response']['type']
    if 'token' in json_obj['response'].keys():
      resp_token = json_obj['response']['token']
    else:
      return resp_message, resp_type
  except json.JSONDecodeError:
    print("Json cannot be decoded.")

  return DataTuple(resp_message, resp_token, resp_type)


def join(username:str, password:str):
  '''
  Create and return a JSON formatted dictionary with the username, password, and token to join the server
  
  '''
  join_dict = {}
  join_dict["join"] = {"username": username, "password": password, "token":""}
  return json.dumps(join_dict)


def posting(token:str, message:str):
  '''
  Create and return a JSON formatted dictionary with the server-sent token and the user message with time stamp
  
  '''
  posting_dict = {}
  posting_dict["token"] = token
  time = post.get_time()
  posting_dict["post"] = {"entry": message, "timestamp": time}
  return json.dumps(posting_dict)


def bio1(token:str, bio:str):
  '''
  Create and return a JSON formatted dictionary with the server-sent token and the user bio with time stamp
  
  '''
  bio1_dict = {}
  bio1_dict["token"] = token
  time = post.get_time()
  bio1_dict["bio"] = {"entry": bio, "timestamp": time}
  return json.dumps(bio1_dict)