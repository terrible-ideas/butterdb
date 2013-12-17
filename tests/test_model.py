import fuckitdb
from . import test_database

database = test_database.create_test_db()

if "FooModel" in database.get_worksheet_names():
    database.db.del_worksheet(database.db.worksheet("FooModel"))


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
