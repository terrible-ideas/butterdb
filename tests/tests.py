from nose.tools import *  # PEP8 asserts
from nose.exc import SkipTest

import butterdb


class MockDB(butterdb.Database):

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
        return butterdb.Cell(row, column, data[row][column])

    def col_values(self, data, column):
        return list(filter(None, zip(*data)[column]))

    def row_values(self, data, row):
        return list(filter(None, data[row]))

    def get_all_values(self, data):
        return data

    def update_cell(self, data, row, column, value):
        data[row][column] = repr(value)

    def update_cells(self, data, cells):
        map(lambda x: self.update_cell(data, x.row, x.column, x.value), cells)


database = MockDB("TestDB")
#database = butterdb.Database("TestDB", "username", "password")


@butterdb.register(database)
class FooModel(butterdb.Model):

    def __init__(self, foo, bar):
        self.foo = self.field(foo)
        self.bar = self.field(bar)


class TestModel(object):

    def test_attrs(self):
        foo, bar = "baz", "fro"
        model = FooModel(foo, bar)
        model.commit()

        assert_equal(model.foo, foo)
        assert_equal(model.bar, bar)

    def test_registration(self):
        assert_in("FooModel", database.get_worksheet_names())

    def test_id(self):
        model = FooModel("a", "b")
        assert model.id

    def test_fields(self):
        assert_equal(list(FooModel.columns.keys()), ["foo", "bar"])

    def test_objects(self):
        assert FooModel.get_instances()

    def test_init_with_id(self):

        instance = FooModel._init_with_id(6, "test", "post")

        assert_equal(instance.id, 6)
        assert_equal(instance._id, 6)

    def test_list_storage(self):
        raise SkipTest("Pending")
        test_list = [1, 2, 3, 4, 5]
        instance = FooModel(test_list, "bar")

        instance.commit()

        my_instance = FooModel.get_instances()[-1]

        assert_equal(my_instance.foo, test_list)

    def test_dict_storage(self):
        raise SkipTest("Pending")
        test_dict = {
            "what": 5,
            "how": "snaz",
            "when": "yesterday"
        }

        instance = FooModel(test_dict, "anything")

        instance.commit()

        my_instance = FooModel.get_instances()[-1]

        assert_equal(my_instance.foo, test_dict)

    def test_modify_existing(self):
        # ensure there is something
        foo, bar = 123, 456
        instance = FooModel(foo, bar)
        instance.commit()

        assert_equal(instance.foo, foo)
        assert_equal(instance.bar, bar)

        # get a new instance to modify from there
        new_instance = FooModel.get_instances()[-1]
        new_instance.foo = bar
        new_instance.commit()

        assert_equal(new_instance.foo, bar)
