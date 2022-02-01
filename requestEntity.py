import json


class RequestHeader:
    __header = {}
    def __init__(self, environments):
        for k, v in environments.items():
            if k.startswith('HTTP_'):
                self.__header[k[5:]] = v

    def __getitem__(self, k):
        return self.__header[k.upper().replace("-","_")]

    def __repl__(self):
        return str(self.__header)

    def __str__(self):
        return str(self.__header)

    def items(self):
        return self.__header.items()

    @property
    def raw(self):
        return self.__header


class RequestEntity:
    '''
    example:
        req = Request(environ)
    '''
    __path = ''
    __ip = ''
    __uri = ''
    __method = ''
    __contentType = ''
    __contentLength = 0
    __body = {}
    __query = {}
    __header = {}

    def __init__(self, environ):
        self.__ip = environ['REMOTE_ADDR']
        self.__method = environ['REQUEST_METHOD']
        self.__path = environ['PATH_INFO']
        self.__uri = environ['fc.request_uri']
        self.__header = RequestHeader(environ)

        try:
            self.__contentType = environ['CONTENT_TYPE']
        except:
            self.__contentType = ""
            print('Resolving content-type error.\nThe original content-type is {}'.format(str(environ['CONTENT_TYPE'])))

        try:
            self.__contentLength = int(environ.get('CONTENT_LENGTH', 0))
        except:
            self.__contentLength = 0
            print('Resolving content-length error.\nThe original content-length is {}'.format(str(environ.get('CONTENT_LENGTH', 0))))

        try:
            if(environ['QUERY_STRING'] != ''):
                self.__query = RequestEntity.queryDecode(environ['QUERY_STRING'])
        except KeyError:
            self.__query = {}
        except:
            self.__query = {}
            print('Resolving url query error.\nThe original url query is {}'.format(str(environ['QUERY_STRING'])))

        if(self.__contentLength > 0):
            if('json' in self.__contentType):
                self.__body = json.loads(environ['wsgi.input'].read(self.__contentLength))
            elif('x-www-form-urlencoded' in self.__contentType):
                self.__body = self.queryDecode(environ['wsgi.input'].read(self.__contentLength).decode('utf-8'))
            # elif('form-data' in self.__contentType):
            elif('text' in self.__contentType):
                self.__body = environ['wsgi.input'].read(self.__contentLength).decode('utf-8')
            else:
                self.__body = environ['wsgi.input'].read(self.__contentLength)

    @staticmethod
    def queryDecode(queryString):
        queriesStr = queryString.split('&')
        queries = {}
        for i in queriesStr:
            q = i.split('=')
            queries[q[0]] = q[1]
        return queries

    @property
    def path(self):
        return self.__path

    @property
    def ip(self):
        return self.__ip
    
    @property
    def uri(self):
        return self.__uri

    @property
    def method(self):
        return self.__method

    @property
    def contentType(self):
        return self.__contentType

    @property
    def contentLength(self):
        return self.__contentLength

    @property
    def body(self):
        return self.__body

    @property
    def query(self):
        return self.__query

    @property
    def header(self):
        return self.__header

