import server
from bson.json_util import loads

def list_data_test_no_data():
    response = server.list_data(MockDB())

    assert response == "[]"

def list_data_test_one_datum():
    data = [
        {"username" : "barney", "emotion" : "2"}
    ]

    response = server.list_data(MockDB(data))
    response = loads(response)

    assert response[0]['data']['2']['value'] == 1

def list_data_test_ignores_data_without_emotions():
    data = [
        {"username" : "barney", "emotion" : "4"},
        {"username" : "barney"},
    ]

    response = server.list_data(MockDB(data))
    response = loads(response)

    assert response[0]['data']['4']['value'] == 1

def list_data_test_two_users():
    data = [
        {"username" : "barney", "emotion" : "3"},
        {"username" : "dino", "emotion" : "3"}
    ]

    response = server.list_data(MockDB(data))
    response = loads(response)

    assert response[0]['data']['3']['value'] == 1

    assert response[1]['data']['3']['value'] == 1

def list_data_test_same_user_two_different_aliases():
    data = [
        {"username" : "barney", "emotion" : "3"},
        {"tagId" : "rubble-meister", "emotion" : "3"}
    ]

    response = server.list_data(MockDB(data), {"rubble-meister" : "barney"})
    response = loads(response)

    assert len(response) == 1
    assert response[0]['data']['3']['value'] == 2

def map_users_together_test_someone_not_in_main_list():

    actual = server.map_users_together({"garbledID" : ["point"]}, {"garbledID" : "Pretty Display Name"})

    assert actual["Pretty Display Name"][0] == "point"

def save_new_test_saves_sent_object():
    db = MockDB()
    request = MockRequest({"username" : "freddy"})

    server.save_new(db, request, MockTime())

    saved = db["happiness"].last_interaction
    assert saved["username"] == "freddy"

def save_new_test_adds_timestamp_before_saving():
    db = MockDB()
    time = MockTime()

    server.save_new(db, MockRequest({}), time)

    saved = db["happiness"].last_interaction
    assert saved["timestamp"] == time.time()

def save_new_test_fails_gracefully_with_no_json():
    request = MockRequest(None)

    response = server.save_new(MockDB(), request)

    assert response["message"] == "this endpoint expects JSON"

def save_new_test_fails_gracefully_with_malformed_json():
    db = MockDB()
    request = ThrowingRequest()

    response = server.save_new(db, request)

    assert response["message"] == "malformed JSON was provided"

def count_data_test_empty():
    result = server.count_data([])

    assert result == {}

def count_data_test_one_point():
    result = server.count_data([1])

    assert result == {1: 1}

def count_data_test_multiple_instances_of_a_point():
    result = server.count_data([1, 1])

    assert result == {1: 2}

def count_data_test_multiple_instances_of_a_point():
    result = server.count_data([1, 2])

    assert result == {1: 1, 2: 1}

def build_dataset_for_graphjs_test_no_data():
    result = server.build_dataset_for_graphjs("bambam", {})

    assert result == {}

def build_dataset_for_graphjs_test_one_point_not_in_known_emotion_map():
    result = server.build_dataset_for_graphjs("bambam", {9999: 3})

    assert result == {"label": "bambam", "data": {9999: {"value": 3}}}

def build_dataset_for_graphjs_test_one_point_with_known_emotion():
    result = server.build_dataset_for_graphjs("bambam", {2: 3})

    assert result == {"label": "bambam", "data": {2: {"value": 3, "label": "Sad", "color": "#1c5ab2"}}}

class MockRequest:
        json = ""
        def __init__(self, jsonToSend):
            self.__class__.json = jsonToSend

class ThrowingRequest:
    pass

class MockDB:
    def __init__(self, mock_data = []):
        self.mockCollection = MockCollection(mock_data)

    def __getitem__(self, item):
        return self.mockCollection

class MockCollection:
    def __init__(self, mock_data):
        self.last_interaction = None
        self.mock_data = mock_data

    def insert_one(self, item):
        self.last_interaction = item

    def last_interaction(self):
        return self.last_interaction

    def find(self):
        return self.mock_data

class MockTime:
    def time(self):
        return 12345
