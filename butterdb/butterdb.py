import gspread

class GDocsConnection(object):
    def __init__(self, email, password):
        self._connection = gspread.login(email, password)
