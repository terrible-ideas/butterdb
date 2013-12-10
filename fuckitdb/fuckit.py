import gspread


class Database(object):
    """docstring for Database"""
    def __init__(self, name, username, password):
        super(Database, self).__init__()
        self.name = name
        self.client = gspread.login(username, password)
        self.db = self.client.open(name)
        self.model = Model


class Model(object):
    """The base object for representing cell data as an object"""
    def _get_own_sheet(self):
        return self.database.__getattr__(self.__name__)

    def __setattr__(self, attr, val):
        return self._get_own_sheet.__setattr__(attr, val)

    def __getattr__(self, attr):
        self.database.

    def register(self, database):
        """Registers the model for storage in the database"""
        self.database = database