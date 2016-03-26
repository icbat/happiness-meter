import server


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

class MockRequest:
        json = ""
        def __init__(self, jsonToSend):
            self.__class__.json = jsonToSend

class ThrowingRequest:
    pass

class MockDB:
    def __init__(self):
        self.mockCollection = MockCollection()

    def __getitem__(self, item):
        return self.mockCollection

class MockCollection:
    def __init__(self):
        self.last_interaction = None

    def insert_one(self, item):
        self.last_interaction = item

    def last_interaction(self):
        return self.last_interaction

class MockTime:
    def time(self):
        return 12345
