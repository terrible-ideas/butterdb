import gspread


class Database(object):
    """docstring for Database"""
    def __init__(self, name, username, password):
        super(Database, self).__init__()
        self.name = name
        self.client = gspread.login(username, password)
        self.db = self.client.open(name)

    def get_worksheet_names(self):
        """Returns a list of worksheet names as strings"""
        return list(map(lambda x: x.title, self.db.worksheets()))

    def register(self):
        """Registers a model for storage in the database"""
        def decorator(f):
            f.database = self
            sheet_name = f.get_name()
            if sheet_name in self.get_worksheet_names():
                f.data = self.db.worksheet(sheet_name)
            else:
                f.data = self.db.add_worksheet(title=sheet_name, rows="100", cols="20")
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

    @classmethod
    def get_name(cls):
        return cls.__name__

    def __setattr__(self, attr, val):
        attrs = {row_value: ind for row_value, ind in enumerate(self.data.row_values(1))}
        if attr in attrs:
            attr_column = attrs[attr]
        else:
            attr_column = len(attrs) + 1
            self.data.update_cell(attr_column, 1, attr)

        print(attr_column, self.id, val)
        self.data.update_cell(attr_column, self.id, val)

    def __getattr__(self, attr):
        pass

    def __repr__(self):
        return "{}: {}".format(self.get_name(), self.id)

    def _add_attr(self, attr):
        pass

    def _post_init(self):
        self.id = self.assign_id()

    def assign_id(self):
        next_id = len(self.data.col_values(1)) + 1
        return next_id