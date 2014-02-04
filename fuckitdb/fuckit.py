import gspread


def register(database):
    """Registers a model for storage in the database"""
    def decorator(f):

        database.register_model(f)
        f.columns = f.generate_columns()
        return f
    return decorator


class Database(object):
    """
    Interacts with Google Spreadsheet.
    Registers models and updates and reads data.
    """

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
        """Gets or creates a worksheet"""
        if sheet_name in self.get_worksheet_names():
            return self.db.worksheet(sheet_name)

        return self.db.add_worksheet(title=sheet_name,
                                     rows="100", cols="20")

    def get_cell(self, data, row, column):
        """Returns the cell object at the given position in the data object"""
        return data.cell(row + 1, column + 1)

    def update_cell(self, data, row, column, value):
        """Update the cell at the given position to the new value"""
        data.update_cell(row + 1, column + 1, value)

    def update_cells(self, data, cells):
        """Updates multiple cells"""
        data.update_cells(cells)

    def col_values(self, data, column):
        """Returns all the values at the given column index. Starts at 0"""
        return data.col_values(column + 1)

    def row_values(self, data, row):
        """Returns all the values at the given row index. Starts at 0"""
        return data.row_values(row + 1)

    def get_all_values(self, data):
        """Returns a nested list of all data"""
        return data.get_all_values()


class Model(object):
    """The base object for representing cell data."""

    def __init__(self, id=None):
        self.fields = {}
        self.changed_values = []
        if id is not None:
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
        """Returns a dict of all the column headers, indice: label"""
        return {label: indice for indice, label in
                enumerate(cls.database.row_values(cls.data, 0))}

    def field(self, name, value=None):
        """Constructs a field. Returns one if it exists, else creates one"""
        new_column = False
        if name in self.columns:
            column = self.columns[name]
        else:
            column = len(self.columns)
            self.__class__.columns[name] = column
            new_column = True

        row = self.id

        if new_column:
            print("Creating {} at {}, {}".format(name, 0, column))
            self.database.update_cell(self.data, 0, column, name)

        new_field = Cell(row, column, value)
        self.fields[name] = new_field

        return new_field

    def commit(self):
        """Commit all changed or new data to the database."""
        print("Commiting")
        print(self.fields)
        cells = []
        for field in filter(lambda x: x.has_changed, self.fields.values()):
            cell = self.database.get_cell(self.data, field.row, field.column)
            print(cell)
            cell.value = field.value
            cells.append(cell)
            field.has_changed = False

        self.database.update_cells(self.data, cells)

    @classmethod
    def get_instances(cls):
        """Returns a list of instances of the class from the database"""
        instances = []
        for n, fields in enumerate(
                filter(lambda x: any(x),
                       cls.database.get_all_values(cls.data))[1:], start=1):
            instances.append(cls(*fields[:len(cls.columns)], id=n))
        return instances

    @property
    def id(self):
        """Sets or returns the object's id for representation in the db"""
        if not hasattr(self, '_id'):
            self._id = len(self.database.col_values(self.data, 0)) or 1
        return self._id


class Cell(object):
    """A value in a spreadsheet in the database"""
    def __init__(self, row, column, value):
        super(Cell, self).__init__()
        self.row = row
        self.column = column
        self.value = value
        self.has_changed = True

    def __setattr__(self, attr, val):
        if attr == "value":
            self.has_changed = True

        super(Cell, self).__setattr__(attr, val)
