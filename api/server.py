from bottle import run, route, debug, template, get, post

@get('/data')
def list():
    return {'message': 'not-yet-implemented'}

@post('/data')
def save_new():
    print("Got something")
    return {'message': 'got it'}

debug(True)
run()
