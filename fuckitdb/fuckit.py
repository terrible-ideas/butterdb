import gspread
import collections


def register(database):
    """Registers a model for storage in the database"""
    def decorator(f):

        database.register_model(f)
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

    def get_cell(self, data, row, column):
        return data.cell(row + 1, column + 1)

    def update_cell(self, data, row, column, value):
        data.update_cell(row, column, value)

    def update_cells(self, data, cells):
        data.update_cells(cells)

    def col_values(self, data, column):
        return data.col_values(column + 1)

    def row_values(self, data, row):
        return data.row_values(row + 1)

    def get_all_values(self, data):
        return data.get_all_values()


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
                enumerate(cls.database.row_values(cls.data, 1))}

    def field(self, name, value=None):
        self.__class__._fields.add(name)

        new_column = False
        if name in self.columns:
            column = self.columns[name]
        else:
            column = len(self.columns)
            self.__class__.columns[name] = column
            new_column = True

        row = self.id

        print("Row: {}".format(row))

        if new_column:
            print("Creating {} at {}, {}".format(name, 0, column))
            self.database.update_cell(self.data, 0, column, name)

        new_field = Cell(row, column, value)
        self.fields[name] = new_field

        return new_field

    def commit(self):
        cells = []
        for field in self.fields.values():
            cell = self.database.get_cell(self.data, field.row, field.column)
            print(cell)
            cell.value = field.value
            cells.append(cell)

        self.database.update_cells(self.data, cells)

    @classmethod
    def get_instances(cls):
        instances = []
        print(cls.database.get_all_values(cls.data))
        for id, fields in enumerate(filter(lambda x: any(x),
                                    cls.database.get_all_values(
                                        cls.data))[1:]):
            print(len(fields))

            instances.append(cls(*filter(None, fields), id=id))
        return instances

    @property
    def id(self):
        if '_id' not in self.__dict__:
            self._id = len(self.database.col_values(self.data, 0)) or 1
        return self._id

class Cell(object):
    def __init__(self, row, column, value):
        super(Cell, self).__init__()
        self.row = row
        self.column = column
        self.value = value


# class Field(object):
#     """A database field"""
#     def __init__(self, name, value, row, column, data):
#         self.name = name
#         self.row = row
#         self.column = column
#         self.value = value

#     def __setattr__(self, attr, val):
#         if attr == "value":
#             self.__dict__["value"] = val
#         else:
#             self.__dict__[attr] = val
