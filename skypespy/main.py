#!/usr/bin/python

import Skype4Py
import logging

skype = Skype4Py.Skype(Transport='x11') 

def isSkypeRunning():
    if not skype.Client.IsRunning:
        logging.info('Skype is not running, trying to start...')
        skype.Client.Start()
    else:
        logging.info('Skype is active, ok')

def attachToSkype():
    skype.FriendlyName = 'SkypeSpy'
    skype.Attach()

if __name__ == '__main__':
    logging.basicConfig(filename = 'skypespy.log', format = '%(asctime)s - %(levelname)s - %(module)s:%(funcName)s - %(message)s', level = logging.DEBUG)

    isSkypeRunning()
    attachToSkype()

    print skype.CurrentUser.FullName
