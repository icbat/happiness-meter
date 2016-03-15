from bottle import run, route, debug, template

@route('/data', method = 'GET')
def list():
    return template('templates/list.tpl')

debug(True)
run(reloader=True)
