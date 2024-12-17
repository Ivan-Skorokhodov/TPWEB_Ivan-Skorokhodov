HELLO_WORLD = b"Hello world!\n"


def simple_app(environ, start_response):
    """Simplest possible application object"""
    status = '200 OK'

    print("----------NEW REQUEST----------")

    print(environ['REQUEST_METHOD'])

    if environ['REQUEST_METHOD'] == 'POST':
        str = environ['wsgi.input'].read().decode('utf-8')

    elif environ['REQUEST_METHOD'] == 'GET':
        str = environ['QUERY_STRING']

    params = str.split('&')
    for param in params:
        print(param)

    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return [HELLO_WORLD]


application = simple_app


class AppClass:

    def __init__(self, environ, start_response):
        self.environ = environ
        self.start = start_response

    def __iter__(self):
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        self.start(status, response_headers)
        yield HELLO_WORLD
