import time

class UserInfo(object):

    def __init__(self, user = None):
        self.data = []
        self.update(user)
 
    def getData(self):
        return self.data

    def setData(self, new_data):
        self.data = new_data

    def diff(self, userattr):
        # check if there are any differences with previous check
        if len(self.data):
            prev_data = self.data[-1][1]
            isDifferent = False
            for prop in prev_data:
                if prev_data[prop] != userattr[prop]:
                    print 'diff', prev_data[prop], userattr[prop]
                    isDifferent = True
                    break
            return isDifferent
        return True

    def update(self, user):
        if user:

            userattr = {
                'skypename': user.Handle,
                'fullname': user.FullName,
                'country': user.Country,
                'status': user.OnlineStatus,
                'homepage': user.Homepage,
            }

            if self.diff(userattr):
                self.data.append( (int(time.time()), userattr, ) )

