import fuckitdb

#if "FooModel" in database.get_worksheet_names():
#    database.db.del_worksheet(database.db.worksheet("FooModel"))


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
            return [['' for i in range(20)] for j in range(100)]

    def get_cell(self, data, row, column):
        print(row, column, len(data[0]), len(data))
        return data[column]

    def col_values(self, data, column):
        return list(zip(*data)[column])

    def row_values(self, data, row):
        return data[row]

    def get_all_values(self, data):
        return data


database = MockDB("TestDB")


@fuckitdb.register(database)
class FooModel(fuckitdb.Model):
    def __init__(self, foo, bar, id=None):
        super(FooModel, self).__init__(id)
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
        print(list(FooModel._fields))
        assert list(FooModel._fields) == ["foo", "bar"]

    def test_objects(self):
        assert FooModel.get_instances()
