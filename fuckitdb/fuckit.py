import gspread


class Database(object):
    """docstring for Database"""
    def __init__(self, name, username, password):
        super(Database, self).__init__()
        self.name = name
        self.client = gspread.login(username, password)
        self.db = self.client.open(name)

    def register(self):
        """Registers a model for storage in the database"""
        def decorator(f):
            f.database = self
            f.data = self.db.worksheet(f.__name__)
            return f
        return decorator        


class ModelMetaclass(type):
    def __call__(cls, *args, **kwargs):
        """Called when you call MyNewClass() """
        obj = type.__call__(cls, *args, **kwargs)
        obj._post_init()
        return obj


class Model(object):
    """The base object for representing cell data as an object"""
    __metaclass__ = ModelMetaclass

    def _get_own_sheet(self):
        return self.database.__getattr__(self.__name__)

    def __setattr__(self, attr, val):
        pass

    def __getattr__(self, attr):
        pass

    def _post_init(self):
        self._id = self.database.assign_id(self)

    def register(self, database):
        """Registers the model for storage in the database"""
        self.database = database