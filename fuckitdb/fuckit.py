import gspread


def register(database):
    """Registers a model for storage in the database"""
    def decorator(f):
        f.database = database
        sheet_name = f.__name__
        if sheet_name in database.get_worksheet_names():
            f.data = database.db.worksheet(sheet_name)
        else:
            f.data = database.db.add_worksheet(title=sheet_name,
                                               rows="100", cols="20")
        return f
    return decorator


class Database(object):
    """docstring for Database"""
    def __init__(self, name, username, password):
        self.name = name
        self.client = gspread.login(username, password)
        self.db = self.client.open(name)

    def get_worksheet_names(self):
        """Returns a list of worksheet names as strings"""
        return list(map(lambda x: x.title, self.db.worksheets()))


class Model(object):
    """The base object for representing cell data as an object"""

    def __setattr__(self, attr, val):
        print(attr, val)

        if attr in self.__dict__ and isinstance(self.__dict__[attr], Field):
            self.__dict__[attr].value = val
        else:
            self.__dict__[attr] = val

    def __getattribute__(self, attr):
        obj = object.__getattribute__(self, attr)
        if isinstance(obj, Field):
            return obj.value
        return obj

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
        return Field(value, row, column, self.data)

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
