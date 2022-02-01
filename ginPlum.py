from responseEntity import ResponseEntity, STATUS_CODE
from requestEntity import RequestEntity
import re


class GinPlum(object):
    def __init__(self, ignoreError=False):
        self.__interfaces = {}
        self.__ignoreError = ignoreError

    def __new__(cls, **kwargs):
        if(not hasattr(cls, '_instance')):
            cls._instance = super().__new__(cls)
        return cls._instance

    def route(self, method, route):
        def decorator(func):
            routeRule = re.sub(r'(<[a-zA-Z]\w+>)', lambda m: r'(?P{}\w+)'.format(m.group(0)), route)
            if(routeRule not in self.__interfaces):
                self.__interfaces[routeRule] = {}
            self.__interfaces[routeRule][method] = func
            return func

        return decorator

    def serve(self, environ):
        self.__request = RequestEntity(environ)
        for route, methods in self.__interfaces.items():
            routeMatch = re.match(route, self.__request.path)
            if(routeMatch != None and routeMatch.span()[1] == len(self.__request.path)):
                if(self.__request.method in methods):
                    kwargs = routeMatch.groupdict()
                    if(self.ignoreError):
                        try:
                            return methods[self.__request.method](**kwargs)
                        except:
                            return self.abort('500')
                    else:
                        return methods[self.__request.method](**kwargs)
                else:
                    return self.abort('405')
        return self.abort('404')

    def abort(self, errCode, msg=''):
        if(errCode in STATUS_CODE):
            return ResponseEntity(body=({'msg': STATUS_CODE[errCode] if (msg == '') else msg}),
                                status='{} {}'.format(errCode, STATUS_CODE[errCode].upper()))
        else:
            return ResponseEntity(body={'msg': msg},
                                status=errCode)

    @property
    def ignoreError(self):
        return self.__ignoreError
    
    @ignoreError.setter
    def ignoreError(self, iEv):
        if(type(iEv) == bool):
            self.__ignoreError = iEv
        else:
            raise ValueError('Argument ignoreError must be bool.')

    @property
    def request(self):
        return self.__request
    
