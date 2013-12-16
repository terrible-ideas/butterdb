import gspread


def register(database):
    """Registers a model for storage in the database"""
    def decorator(f):
        database.register_model(f)
        return f
    return decorator


class Database(object):
    """docstring for Database"""
    def __init__(self, name, username, password):
        self.models = {}
        self.name = name
        self.client = gspread.login(username, password)
        self.db = self.client.open(name)

    def get_worksheet_names(self):
        """Returns a list of worksheet names as strings"""
        return list(map(lambda x: x.title, self.db.worksheets()))

    def register_model(self, model):
        """Registers a model for use with the database"""
        model.database = self
        sheet_name = model.__name__
        self.models[sheet_name] = model

        model.data = self.get_or_create_worksheet(sheet_name)

    def get_or_create_worksheet(self, sheet_name):
        if sheet_name in self.get_worksheet_names():
            return self.db.worksheet(sheet_name)

        return self.db.add_worksheet(title=sheet_name,
                                     rows="100", cols="20")


class Model(object):
    """The base object for representing cell data as an object"""
    _fields = {}

    def __setattr__(self, attr, val):
        if attr in self._fields and attr in self.__dict__:
            self.__dict__[attr].value = val
        else:
            self.__dict__[attr] = val

    def __getattribute__(self, attr):
        fields = object.__getattribute__(self, '_fields')
        if attr in fields:
            return fields[attr].value
        return object.__getattribute__(self, attr)

    def field(self, name, value=None):
        columns = self.data.row_values(1)
        if name in columns:
            column = columns.index(name) + 1
        else:
            column = len(columns) + 1

        row = self.id + 1
        print("ID: {}".format(self.id))
        print("Creating {} at {}, {}".format(name, row, column))
        self.data.update_cell(1, column, name)

        new_field = Field(value, row, column, self.data)
        self.__class__._fields[name] = new_field

        return new_field

    @property
    def id(self):
        if '_id' not in self.__dict__:
            self._id = len(self.data.col_values(1)) or 1
        return self._id


class Field(object):
    """A database field"""
    def __init__(self, value, row, column, data):
        self.data = data
        self.row = row
        self.column = column
        self.value = value

    def __setattr__(self, attr, val):
        if attr == "value":
            self.__dict__["value"] = val
            self.data.update_cell(self.row, self.column, val)
            print("Updating {}, {} to be {}".format(self.row,
                                                    self.column, val))
        else:
            self.__dict__[attr] = val
