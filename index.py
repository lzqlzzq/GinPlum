from api import service


def handler(environ, start_response):
    res = service.serve(environ)

    start_response(res.status, res.header)
    return [res.body]

