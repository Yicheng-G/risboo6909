#!/usr/bin/python

from userinfo import UserInfo

import Skype4Py
import logging, time

skype = Skype4Py.Skype(Transport='x11') 
userdata = {}

REFRESH_DELAY = 10

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
            uinfo = userdata.get(friend.Handle, UserInfo())
            uinfo.update(friend)
#            print friend.Handle, friend.FullName, friend.Country, friend.OnlineStatus
    except:
        pass

if __name__ == '__main__':
    logging.basicConfig(filename = 'skypespy.log', format = '%(asctime)s - %(levelname)s - %(module)s:%(funcName)s - %(message)s',
                             level = logging.INFO)


    isSkypeRunning()
    attachToSkype()

    while True:
        try:
            refreshFriends()
            timestamp = time.ctime(time.time())
            logging.info('Refreshed friends list at %s for user %s' % (timestamp, skype.CurrentUser.FullName))
            print 'Refreshed friends list at %s for user %s' % (timestamp, skype.CurrentUser.FullName)
            time.sleep(REFRESH_DELAY)
        except KeyboardInterrupt:
            print 'break'
            break

