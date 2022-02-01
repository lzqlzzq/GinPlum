import json


STATUS_CODE = { '100': 'Continue',
                '101': 'Switching Protocols',
                '200': 'OK',
                '201': 'Created',
                '202': 'Accepted',
                '203': 'No Content',
                '204': 'Reset Content',
                '205': 'Partial Content',
                '206': 'Multiple Choices',
                '300': 'Moved Permanently',
                '301': 'Found',
                '302': 'See Other',
                '303': 'Not Modified',
                '304': 'Use Proxy',
                '305': 'Temporary Redirect',
                '307': 'Bad Request',
                '400': 'Unauthorized',
                '401': 'Payment Required',
                '402': 'Forbidden',
                '403': 'Not Found',
                '404': 'Method Not Allowed',
                '405': 'Not Acceptable',
                '406': 'Proxy Authentication Required',
                '407': 'Request Timeout',
                '408': 'Conflict',
                '409': 'Gone',
                '410': 'Length Required',
                '411': 'Precondition Failed',
                '412': 'Payload Too Large',
                '413': 'URI Too Long',
                '414': 'Unsupported Media Type',
                '415': 'Range Not Satisfiable',
                '416': 'Expectation Failed',
                '417': 'Upgrade Required',
                '426': 'Internal Server Error',
                '500': 'Not Implemented',
                '501': 'Bad Gateway',
                '502': 'Service Unavailable',
                '503': 'Gateway Timeout',
                '504': 'HTTP Version Not Supported'}


class ResponseEntity:

    def __init__(self, body, status='200 OK', header={}, contentType=''):
        self.__header = [(k, v) for k, v in header.items()]
        self.__status = status

        if(contentType != ''):
            self.header.append(('Content-type', contentType))
            return self

        if(type(body) == dict or type(body) == list):
            self.header.append(('Content-type', 'application/json; charset=utf-8'))
            self.__body = json.dumps(body).encode('utf-8')
        elif(type(body) == str):
            self.header.append(('Content-type', 'text/plain; charset=utf-8'))
            self.__body = body.encode('utf-8')
        elif(type(body) == bytes):
            self.header.append(('Content-type', 'application/octet-stream'))
            self.__body = body
        else:
            self.__body = body

    @property
    def header(self):
        return self.__header

    @property
    def status(self):
        return self.__status

    @property
    def body(self):
        return self.__body

