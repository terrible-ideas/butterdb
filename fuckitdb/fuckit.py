import gspread


def register(database):
    """Registers a model for storage in the database"""
    def decorator(f):
        f.database = database
        sheet_name = f.__name__
        database.models[sheet_name] = f
        if sheet_name in database.get_worksheet_names():
            f.data = database.db.worksheet(sheet_name)
        else:
            f.data = database.db.add_worksheet(title=sheet_name,
                                               rows="100", cols="20")
        f.columns = f.generate_columns()
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


class Model(object):
    """The base object for representing cell data as an object"""
    _fields = set()

    def __init__(self, id=None):
        self.fields = {}
        if id:
            self._id = id

    def __setattr__(self, attr, val):

        if attr != "fields" and attr in self.fields and attr in self.__dict__:
            self.__dict__[attr].value = val
        else:
            self.__dict__[attr] = val

    def __getattribute__(self, attr):
        if hasattr(self, 'fields'):
            fields = object.__getattribute__(self, 'fields')
            if attr in fields:
                return fields[attr].value
        return object.__getattribute__(self, attr)

    @classmethod
    def generate_columns(cls):
        return {label: indice + 1 for indice, label in
                enumerate(cls.data.row_values(1))}

    def field(self, name, value=None):
        self.__class__._fields.add(name)

        new_column = False
        if name in self.columns:
            column = self.columns[name]
        else:
            column = len(self.columns) + 1
            self.__class__.columns[name] = column

        row = self.id + 1

        if new_column:
            print("Creating {} at {}, {}".format(name, 1, column))
            self.data.update_cell(1, column, name)

        new_field = Field(name, value, row, column, self.data)
        self.fields[name] = new_field

        return new_field

    def commit(self):
        cells = []
        for field in self.fields.values():
            cell = self.data.cell(field.row, field.column)
            cell.value = field.value
            cells.append(cell)

        self.data.update_cells(cells)

    @classmethod
    def get_instances(cls):
        instances = []
        for id, fields in enumerate(cls.data.get_all_values()[1:]):
            instances.append(cls(*fields, id=id + 1))
        return instances

    @property
    def id(self):
        if '_id' not in self.__dict__:
            self._id = len(self.data.col_values(1)) or 1
        return self._id


class Field(object):
    """A database field"""
    def __init__(self, name, value, row, column, data):
        self.name = name
        self.data = data
        self.row = row
        self.column = column
        self.value = value

    def __setattr__(self, attr, val):
        if attr == "value":
            self.__dict__["value"] = val
        else:
            self.__dict__[attr] = val
