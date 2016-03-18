from bottle import Bottle, request, static_file, template
import argparse
from bottle.ext.mongo import MongoPlugin
from bson.json_util import dumps
from os import environ
import time

print ("Initializing")
app = Bottle()
print ("Reading db configuration from 'mongo_uri' environment variable")
mongo_uri = environ["mongo_uri"]
print ("Connecting to mongo")
plugin = MongoPlugin(uri=mongo_uri, db="mydb", json_mongo=True)
app.install(plugin)

@app.get('/js/:path#.+#')
def server_static(path):
    print ('loading static js: ' + path)
    return static_file(path, root = 'bower_components')

@app.get('/')
@app.get('/index.html')
@app.get('/happiness-data')
def list_data(mongodb):
    print ("Fetching all happiness data from DB")
    raw = mongodb['happiness'].find()
    data = dumps(raw)
    return template('graph', data=data)

@app.post('/happiness-data')
def save_new(mongodb):
    try:
        data_point = request.json
    except:
        return {"message": "malformed JSON was provided"}
    if data_point is None:
        print ("No JSON posted")
        return {"message": "this endpoint expects JSON"}

    print ("Adding timestamp to data")
    data_point['timestamp'] = time.time()
    print ("JSON received:")
    print (dumps(data_point))
    print ("Saving to mongodb")
    mongodb['happiness'].insert(data_point)
    return dumps(data_point)

@app.get('/users')
def list_users():
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
