from bottle import run, route, debug, template, get, post, request
import argparse

@get('/happiness-data')
def list():
    return {'message': 'not-yet-implemented'}

@get('/users')
def list():
    return {'message': 'not-yet-implemented'}

@post('/happiness-data')
def save_new():
    print ("### Start transmission ###")
    print_value ("request", request)
    print_value ("request.json", request.json)
    print_map ("request.POST", request.POST)
    print_map ("request.POST.files", request.POST.files)
    print_map ("request.POST.forms", request.POST.forms)
    print_map ("request.forms", request.forms)
    print_value ("key's value", request.json['key'])
    print ("### End transmission ###")
    print("\n\n")

    return {'message': 'got it'}

def print_value(name, value):
    print ("## " + str(name))
    print (value)
    print ("\n")

def print_map(name, map):
    print ("## " + str(name))
    print ("Found a dictionary")
    for key in map:
        print("  -   " + str(key) + " : " + str(map[key]))
    print ("\n")


@post('/users/link')
def link_users():
    return {'message': 'not-yet-implemented, use /happiness-data for testing'}

parser = argparse.ArgumentParser()
parser.add_argument('--port', type=int, default="5000")
parser.add_argument('--host', default="127.0.0.1")
args = parser.parse_args()

run(port=args.port, host=args.host)
