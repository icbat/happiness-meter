from bottle import run, route, debug, template, get, post
import argparse

@get('/data')
def list():
    return {'message': 'not-yet-implemented'}

@post('/data')
def save_new():
    print("Got something")
    return {'message': 'got it'}

parser = argparse.ArgumentParser()
parser.add_argument('--port', type=int, default="5000")
parser.add_argument('--host', default="127.0.0.1")
args = parser.parse_args()

run(port=args.port, host=args.host)
