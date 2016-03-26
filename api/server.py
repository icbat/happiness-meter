from bottle import Bottle, request, static_file, template, debug
import argparse
from bottle.ext.mongo import MongoPlugin
from bson.json_util import dumps, loads
from os import environ
import time

print ("Initializing")
app = Bottle()

fake_user_map = {
    "4572bda7c4980" : "SuperWes",
    "45e8e6a8e4b80" : "Evan",
    "49011c2952f80" : "James M.",
    "453dd1bb91b80" : "Mitch",
    "4b9b06a7c4880" : "Tice"
}

@app.get("/css/:path#.+#")
def server_static(path):
    print ("loading static css: " + path)
    return static_file(path, root = "bower_components")

@app.get("/js/:path#.+#")
def server_static(path):
    print ("loading static js: " + path)
    return static_file(path, root = "bower_components")

@app.get("/images/:path#.+#")
def server_static(path):
    print ("loading static image: " + path)
    return static_file(path, root = "images")

@app.get("/")
@app.get("/index.html")
def index():
    return template('graph')

@app.get("/happiness-data")
def list_data(mongodb, user_map = fake_user_map):
    data_points = fetch_data(mongodb)
    data_by_user = group_data_by_user(data_points)
    data_by_user = map_users_togeter(data_by_user, user_map)

    datasets = []
    for user in data_by_user:
        dataset = {}
        emotions = {
            1 : {
                "label" : "Angry",
                "color": "#ed1c24",
                "value": 0
            },

            2 : {
                "label" : "Sad",
                "color": "#1c5ab2",
                "value": 0
            },

            3 : {
                "label" : "Meh",
                "color": "#6F84A7",
                "value": 0
            },

            4 : {
                "label" : "Happy",
                "color": "#3bf276",
                "value": 0
            },

            5 : {
                "label" : "Ecstatic",
                "color": "#FEDF09",
                "value": 0
            }
        }

        dataset["label"] = user
        for point in data_by_user[user]:
            emotions[point]["value"] = emotions[point]["value"] + 1

        dataset["data"] = emotions
        datasets.append(dataset)

    return dumps(datasets)

def fetch_data(mongodb):
    print ("Fetching all happiness data from DB")
    raw = mongodb["happiness"].find()

    # This essentially casts from "json" to string back to json. /shrugface
    data = dumps(raw)
    data_points = loads(data)
    return data_points

def group_data_by_user(data_points):
    data_by_user = {}
    print ("Found " + str(len(data_points)) + " data points")
    for document in data_points:
        identifier = None
        if "username" in document:
            identifier = str(document["username"])
        if "tagId" in document:
            identifier = str(document["tagId"])

        if identifier is not None:
            if identifier not in data_by_user:
                data_by_user[identifier] = []
            if "emotion" in document:
                data_by_user[identifier].append(int(document["emotion"]))
        else:
            print("Could not find a username or tagId for:  " + str(document))
    return data_by_user

def map_users_togeter(data_by_user, user_map):
    dead_users = []
    for identifier in data_by_user:
        if identifier in user_map:
            mapped_username = user_map[identifier]
            print ("Alias for " + identifier + " is " + mapped_username)
            data_by_user[mapped_username].extend(data_by_user[identifier])
            dead_users.append(identifier)
    for user in dead_users:
        del data_by_user[user]
    return data_by_user

@app.post("/happiness-data")
def save_new(mongodb, bottleRequest = request, systemTime = time):
    try:
        data_point = bottleRequest.json
        print ("Saving new from " + str(data_point))
    except:
        return {"message": "malformed JSON was provided"}
    if data_point is None:
        print ("No JSON posted")
        return {"message": "this endpoint expects JSON"}

    print ("Adding timestamp to data")
    data_point["timestamp"] = systemTime.time()
    print ("JSON received:")
    print (dumps(data_point))
    print ("Saving to mongodb")
    mongodb["happiness"].insert_one(data_point)
    print ("Save was successful!")
    return dumps(data_point)

@app.get("/users")
def list_users():
    return {"message": "not-yet-implemented"}

@app.post("/users/link")
def link_users():
    return {"message": "not-yet-implemented, use /happiness-data for testing"}

if __name__ == "__main__":
    print ("Reading db configuration from 'mongo_uri' environment variable")
    mongo_uri = environ["mongo_uri"]
    print ("Connecting to mongo")
    plugin = MongoPlugin(uri=mongo_uri, db="mydb", json_mongo=True)
    app.install(plugin)

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default="5000")
    parser.add_argument("--host", default="127.0.0.1")
    args = parser.parse_args()

    debug(True)

    print ("Starting the server")
    app.run(port=args.port, host=args.host)
    print ("Shutting down")
