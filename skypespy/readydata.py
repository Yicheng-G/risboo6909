""" Contains data ready to be dumped to disk """

from userinfo import UserInfo
import cPickle as pickle

import os, logging

logger = logging.getLogger('skypespy')

class ReadyData(object):

    DATA_DIR = 'data'

    def __init__(self, save_after = 2):
        self.userdata = {}
        if save_after < 2:
            save_after = 2
        self.save_after = save_after
        # create data directory
        if not os.path.isdir(ReadyData.DATA_DIR):
            os.mkdir(ReadyData.DATA_DIR)

    def getUser(self, name):
        return self.userdata.setdefault(name, UserInfo())
 
    def dumpData(self, force = False):
        # dump all the data except the last record
        for username in self.userdata.keys():
            user = self.userdata[username]
            if len(user.getData()) >= self.save_after or force:
                logger.info('starting data dump for user %s' % user)
                if not force:
                    head, tail = user.getData()[:len(user.getData()) - 1], user.getData()[:-1] 
                else:
                    head = user.getData()
                # dump head items and keep tail item
                path = os.path.join(ReadyData.DATA_DIR, username)
                if not os.path.isdir(path):
                    os.mkdir(path)
                for item in head:
                    fname = os.path.join(path, 'data.%s.%d' % (username, item[0]))                  
                    f = open(fname, 'wb')
                    pickle.dump(item, f, pickle.HIGHEST_PROTOCOL)
                    f.close()
                if not force:
                    user.setData(tail)
                logger.info('data dump finished')

