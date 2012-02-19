import BaseHTTPServer, time


class DataReader(object):

    def __init__(self):
        pass


dataReader = DataReader()

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(s):
        pass



myServer = BaseHTTPServer.HTTPServer(('localhost', 11003), MyHandler)

try:
    myServer.serve_forever()
except KeyboardInterrupt:
    pass

myServer.server_close()

