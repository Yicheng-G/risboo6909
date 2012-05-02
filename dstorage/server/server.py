"""
    Distributed storage server.
"""

import tornado.ioloop
import tornado.web
import xmlrpclib

class RootHandler(tornado.web.RequestHandler):

    def get(self):
        # debug purposes handlers
        userId = self.get_argument('user')
        action = self.get_argument('action')
        password = self.get_argument('pass')
        self.write('%s for user %s' % (action, userId))
        if action == 'files':
            # print all files of userId
            pass

    def post(self):
        # xmlrpc handler goes here
        try: 
            params, method_name = xmlrpclib.loads(self.request.body)
        except:
            raise Exception('bad request')
        try:
            method = getattr(self, method_name)
        except:
            raise Exception('%s is not a valid method' % method_name)

        response = method(*params)
        response_xml = xmlrpclib.dumps((response, ), methodresponse = True)
        print response_xml
        self.set_header('Content_Type', 'text/xml')
        self.write(response_xml)

class XMLRPCHandler(RootHandler):

    def FLIST(self, userId, password):
        # returns files list for a given user
        self.write('FLIST')
        return 2 

class Server(object):

    def __init__(self):
        self.app = tornado.web.Application([(r'/', XMLRPCHandler),])
        self.app.listen(8888)

    def runServer(self):
        tornado.ioloop.IOLoop.instance().start()


