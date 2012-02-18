#!/usr/bin/python

from userinfo import UserInfo
from readydata import ReadyData
from aggr import aggregate

import Skype4Py
import logging, time
import logging.handlers

skype = Skype4Py.Skype(Transport='x11') 
readyData = ReadyData(save_after = 4)

REFRESH_DELAY = 2
DATA_DIR = 'data'

def isSkypeRunning():
    if not skype.Client.IsRunning:
        logging.info('Skype is not running, trying to start...')
        skype.Client.Start()
    else:
        logging.info('Skype is active, ok')

def attachToSkype():
    skype.FriendlyName = 'SkypeSpy'
    skype.Attach()

def refreshFriends():
    try:
        for friend in skype.Friends:
            uinfo = readyData.getUser(friend.Handle)
            uinfo.update(friend)
#            print friend.Handle, friend.FullName, friend.Country, friend.OnlineStatus
    except:
        pass

def createLogger():
    logger = logging.getLogger('skypespy')
    logger.setLevel(logging.INFO)
    rfh = logging.handlers.RotatingFileHandler('skypespy.log', maxBytes = 1000000, backupCount = 2)
    rfh.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s:%(funcName)s - %(message)s')
    rfh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(rfh)
    logger.addHandler(ch)
    return logger

if __name__ == '__main__':


    logger = createLogger()

    isSkypeRunning()
    attachToSkype()

    while True:

        try:

            refreshFriends()

            readyData.dumpData()
            aggregate(DATA_DIR)

            timestamp = time.ctime(time.time())
            logger.info('Refreshed friends list at %s for user %s' % (timestamp, skype.CurrentUser.FullName))
            time.sleep(REFRESH_DELAY)

        except KeyboardInterrupt:
            readyData.dumpData(force = True)
            aggregate(DATA_DIR)
            break
