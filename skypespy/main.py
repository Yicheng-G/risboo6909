#!/usr/bin/python

from userinfo import UserInfo

import Skype4Py
import logging, time

skype = Skype4Py.Skype(Transport='x11') 
userdata = {}

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
            userdata[friend.Handle] = UserInfo(friend) 
            print friend.Handle, friend.FullName, friend.Country
    except:
        pass

if __name__ == '__main__':
    logging.basicConfig(filename = 'skypespy.log', format = '%(asctime)s - %(levelname)s - %(module)s:%(funcName)s - %(message)s',
                             level = logging.DEBUG)

    isSkypeRunning()
    attachToSkype()

    while True:
        logging.info('Refreshing friends list...')
        refreshFriends()
        #print skype.CurrentUser.FullName
        time.sleep(2)
        logging.info('Done refreshing!')

