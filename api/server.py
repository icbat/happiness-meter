from bottle import Bottle, request
import argparse
from bottle.ext.mongo import MongoPlugin
from bson.json_util import dumps
from os import environ

print ("Initializing")
app = Bottle()
print ("Reading db configuration from 'mongo_uri' environment variable")
mongo_uri = environ["mongo_uri"]
print ("Connecting to mongo")
plugin = MongoPlugin(uri=mongo_uri, db="mydb", json_mongo=True)
app.install(plugin)

@app.get('/happiness-data')
def list(mongodb):
    print ("Fetching all happiness data from DB")
    return dumps(mongodb['happiness'].find())

@app.post('/happiness-data')
def save_new():
    data_point = request.json
    if data_point is None:
        print ("No JSON posted")
        return {"message": "this endpoint expects JSON, try again!"}

    print ("JSON received:")
    print (dumps(data_point))
    return dumps(data_point)

@app.get('/users')
def list():
    return {'message': 'not-yet-implemented'}

@app.post('/users/link')
def link_users():
    return {'message': 'not-yet-implemented, use /happiness-data for testing'}


parser = argparse.ArgumentParser()
parser.add_argument('--port', type=int, default="5000")
parser.add_argument('--host', default="127.0.0.1")
args = parser.parse_args()

print ("Starting the server")
app.run(port=args.port, host=args.host)
print ("Shutting down")
