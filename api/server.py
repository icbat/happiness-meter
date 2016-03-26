from bottle import Bottle, request, static_file, template, debug
import argparse
from bottle.ext.mongo import MongoPlugin
from bson.json_util import dumps, loads
from os import environ
import time

print ("Initializing")
app = Bottle()

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
def list_data(mongodb):
    print ("Fetching all happiness data from DB")
    raw = mongodb["happiness"].find()

    fake_user_map = {
        "4572bda7c4980" : "SuperWes",
        "45e8e6a8e4b80" : "Evan",
        "49011c2952f80" : "James M.",
        "453dd1bb91b80" : "Mitch",
        "4b9b06a7c4880" : "Tice"
    }

    # This essentially casts from "json" to string back to json. /shrugface
    data = dumps(raw)
    parsed = loads(data)

    # IN
    # {
    # timestamp
    # tagId or username
    # emotion
    # }

    data_by_user = {}

    for document in parsed:
        identifier = None
        if "username" in document:
            identifier = str(document["username"])
        if "tagId" in document:
            identifier = str(document["tagId"])
            if identifier in fake_user_map:
                identifier = fake_user_map[identifier]

        if identifier is not None:
            if identifier not in data_by_user:
                data_by_user[identifier] = []
            data_by_user[identifier].append(int(document["emotion"]))

    # Step in the middle:
    # {identifier : data[emotion1, emotion2, emotion3]}

    # ecstatic happy meh sad angry
    label = "label"
    color = "color"
    value = "value"

    datasets = []
    for user in data_by_user:
        dataset = {}
        emotions = {
            1 : {
                label : "Angry",
                color: "#ed1c24",
                value: 0
            },

            2 : {
                label : "Sad",
                color: "#1c5ab2",
                value: 0
            },

            3 : {
                label : "Meh",
                color: "#6F84A7",
                value: 0
            },

            4 : {
                label : "Happy",
                color: "#3bf276",
                value: 0
            },

            5 : {
                label : "Ecstatic",
                color: "#FEDF09",
                value: 0
            }
        }

        dataset["label"] = user
        # data_by_user[user]
        for point in data_by_user[user]:
            emotions[point][value] = emotions[point][value] + 1

        dataset["data"] = emotions
        datasets.append(dataset)

# GOAL
# 	{
# // 		fillColor : "rgba(151,187,205,0.2)",
# // 		strokeColor : "rgba(151,187,205,1)",
# // 		pointColor : "rgba(151,187,205,1)",
# // 		pointStrokeColor : "#fff",
# // 		pointHighlightFill : "#fff",
# // 		pointHighlightStroke : "rgba(151,187,205,1)",
# // 		label: "My Second dataset",
# // 		data : [randomScalingFactor(),randomScalingFactor(),randomScalingFactor(),randomScalingFactor(),randomScalingFactor(),randomScalingFactor(),randomScalingFactor()]
# // 	}

    return dumps(datasets)

@app.post("/happiness-data")
def save_new(mongodb):
    try:
        data_point = request.json
    except:
        return {"message": "malformed JSON was provided"}
    if data_point is None:
        print ("No JSON posted")
        return {"message": "this endpoint expects JSON"}

    print ("Adding timestamp to data")
    data_point["timestamp"] = time.time()
    print ("JSON received:")
    print (dumps(data_point))
    print ("Saving to mongodb")
    mongodb["happiness"].insert(data_point)
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
