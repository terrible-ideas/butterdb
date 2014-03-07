import fuckitdb


class MockDB(fuckitdb.Database):
    """A Mock Database that doesn't connect to Google Spreadhset"""
    def __init__(self, name):
        self.models = {}
        self.name = name
        self.worksheets = {}

    def get_worksheet_names(self):
        return list(self.models.keys())

    def get_or_create_worksheet(self, sheet_name):
        if sheet_name in self.worksheets:
            return self.worksheets[sheet_name]
        else:
            return [['' for i in range(100)] for j in range(20)]

    def get_cell(self, data, row, column):
        print(len(data))
        print(row)
        return fuckitdb.Cell(row, column, data[row][column])

    def col_values(self, data, column):
        return list(filter(None, zip(*data)[column]))

    def row_values(self, data, row):
        return list(filter(None, data[row]))

    def get_all_values(self, data):
        return data

    def update_cell(self, data, row, column, value):
        data[row][column] = value

    def update_cells(self, data, cells):
        map(lambda x: self.update_cell(data, x.row, x.column, x.value), cells)


database = MockDB("TestDB")
#database = fuckitdb.Database("TestDB", "username", "password")


@fuckitdb.register(database)
class FooModel(fuckitdb.Model):
    def __init__(self, foo, bar):
        self.foo = self.field("foo", foo)
        self.bar = self.field("bar", bar)


class TestModel(object):
    def test_attrs(self):
        foo, bar = "baz", "fro"
        model = FooModel(foo, bar)
        model.commit()

        print(repr(model.foo), repr(model.bar))

        assert model.foo == foo
        assert model.bar == bar

    def test_registration(self):
        assert "FooModel" in database.get_worksheet_names()

    def test_id(self):
        model = FooModel("a", "b")
        assert model.id

    def test_fields(self):
        assert list(FooModel.columns.keys()) == ["foo", "bar"]

    def test_objects(self):
        assert FooModel.get_instances()

    def test_init_with_id(self):

        instance = FooModel._init_with_id(6, "test", "post")

        assert instance.id == 6
        assert instance._id == 6
