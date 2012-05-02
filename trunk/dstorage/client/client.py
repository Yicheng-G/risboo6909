import xmlrpclib

class Client(object):

    def __init__(self):
        pass

    def request(self):
        remote = xmlrpclib.ServerProxy('http://localhost:8888/')
        answer = remote.FLIST('risboo6909', 'pass')
        print answer

