from responseEntity import ResponseEntity
from ginPlum import GinPlum
import logging


# 和FC文档中一样记录日志
logger = logging.getLogger()


service = GinPlum()
service.ignoreError = False # 设置GinPlum是否屏蔽业务代码中的运行时错误输出
# 若屏蔽且API代码运行时出现错误，则返回HTTP 500，生产环境建议设为"True"


# Hello World~
# 最简单的返回静态数据的API，可直接通过FC控制台显示的“公网访问地址”调用
@service.route('GET', '/hello') # 设置该接口的HTTP方法与路由
def hello():
    # 返回的必须是一个"ResponseEntity"对象
    return ResponseEntity('Hello World!')
# 来尝试向URI"/hello"发送GET请求~


# 获取请求体信息
# 对同样的路由绑定不同的请求方法
@service.route('POST', '/hello')
def post_hello(): # 业务函数不可与之前的重名
    # 由于不知道请求参数是否有效，在获取参数时使用try是很必要的
    try:
        # 所有的请求信息被解析并封装在了GinPlum实例的成员变量中
        name = service.request.body
    except KeyError:
        return service.abort('400', msg='Argument invaild.') # 这将会返回一个400错误

    return ResponseEntity('Hello {}!'.format(name))
# 试试向URI"/hello"发送POST请求，下有示例~
'''
  注：GinPlum会识别请求的content-type，并将请求体做相应的转换，以下是目前支持的content-type：
  |                 content-type与python类型对照表                 |
  |       content-type       |    python type   |     example     |
  |     application/json     |   dict or list   | {"msg": "Gin"}  |
  |        text/plain        |       str        |       Gin       |
  |  x-www-form-urlencoded   |       dict       |    liquor=Gin   |
  |         other...         |       bytes      |
  在下面，你可能也会注意到，对返回信息GinPlum也会做相应的处理，
  但list或dict中只可包含str不可包含其它无法迭代的类型，否则会出现json解析错误。
'''


# 在URI中增加参数
# 参数名可以是用尖括号包裹的字母、数字、下划线（但只能以字母开头），如"<userName>"，GinPlum会识别您的参数并传入业务函数内
@service.route('GET', '/hi/<userName>')
def helloUser(userName):
    return ResponseEntity('Hi {}!'.format(userName))
# 来尝试向URI"/hi/Gin"发送GET请求


# 获取请求头
@service.route('GET', '/request/headers')
def req_header():
    headers = service.request.header
    rtnBody = {}
    rtnBody['request-headers'] = {}
    try:
        # GinPlum对请求头进行过处理，所以可以像访问字典一样访问请求头信息，并在key中自由使用大小写与下划线
        rtnBody['request-headers']['ACCEPT_LANGUAGE'] = headers['accept-language']
        rtnBody['request-headers']['HOST'] = headers['host']
        rtnBody['request-headers']['ORIGIN'] = headers['origin']
        rtnBody['request-headers']['REFERER'] = headers['referer']
    except KeyError:
        # 可以使用GinPlum实例的abort()函数来返回错误，详见“错误处理”
        return service.abort('400', msg='Argument invaild.')

    # 请求头可以使用raw属性获得字典类型的请求头
    # FC会对请求头进行处理，故与传入的请求头会有所不符，详见https://help.aliyun.com/document_detail/74756.html
    rtnBody['msg'] = 'JSON serialized string of request header:\n{}'.format(str(headers.raw))

    return ResponseEntity(rtnBody)
# 尝试向"/request/headers"发送GET请求，并填入自定义的header吧


# 获取请求的Query参数
@service.route('GET', '/request/queries')
def req_query():
    try:
        # GinPlum会解析url后的query string，并转成字典
        base = service.request.query['base']
        auxiliary = service.request.query['auxiliary']
    except KeyError:
        return service.abort('400', msg='Argument invaild.')

    return ResponseEntity('The "GinPlum" is a kind of cocktail prepared with base liquor of {} with {} as auxiliary.'.format(base, auxiliary))
# 试试用url"/request/queries?base=Gin&auxiliary=Plum"发送请求~


# 获取原始请求元信息
# 包括路径、uri、请求者ip、请求方法、内容类型、内容长度
@service.route('PUT', '/request/metadata')
def metadata():
    rtnBody = {}
    rtnBody['request-path'] = service.request.path
    rtnBody['request-uri'] = service.request.uri
    rtnBody['request-ip'] = service.request.ip
    rtnBody['request-method'] = service.request.method
    rtnBody['request-content-type'] = service.request.contentType
    rtnBody['request-content-length'] = service.request.contentLength

    return ResponseEntity(rtnBody)
# 试试向"/request/metadata"发送PUT请求吧（别忘了在触发器管理中勾选允许PUT）


# 自定义应答头
@service.route('GET', '/response/header')
def res_header():
    # 与请求相同，应答头也用字典存储，由GinPlum处理后返回给FC
    header = { "header1": "value1",
                "header2": "value2",
                "set-cookie": "session=120382134928"
    }
    # 在ResponseEntity的构造函数中带上header参数以自定义应答头
    return ResponseEntity('This response is with some custom headers!', header=header)
# 打开F12开发者工具，向"/response/header"发送GET请求，并观察这个应答的应答头


# 自定义应答content-type
@service.route('GET', '/response/contentType')
def res_content_type():
    # 在ResponseEntity的构造函数中带上contentType参数以自定义内容类型
    # 若没有该参数，GinPlum将根据传入的应答体自行增加content-type，具体见content-type与python类型对照表
    return ResponseEntity('This response is with custom content-type!', contentType='text/html; charset=utf-8')
# 向"/response/contentType"发送GET请求，尝试下载这个应答内容，看看后缀名是html文件还是txt文件


# 自定义应答状态
@service.route('GET', '/response/status')
def res_status():
    # 在ResponseEntity的构造函数中带上status参数以自定义内容类型，若没有该参数，默认为"200 OK"
    # http 状态由一个三位数状态码与一个小短语组成，详见RFC7231
    return ResponseEntity('This response is with custom status!', status='201 CREATED')
# 向"/response/status"发送GET请求，观察应答的状态码


# 错误处理
@service.route('GET', '/response/error')
def handle_error():
    # 使用GinPlum实例对象的abort参数，参数为http状态码与一小段便于诊断的信息（可选）
    return service.abort('529', msg='Server error.')

    # GinPlum内置了RFC7231定义的40种状态码，也可直接使用，如：
    #      return service.abort('401')
# 试试向"/response/error"发送GET请求，观察应答

