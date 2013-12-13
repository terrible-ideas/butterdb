import fuckitdb
from . import test_database

database = test_database.create_test_db()

@database.register()
class FooModel(fuckitdb.Model):
    def __init__(self, foo, bar):
        self.foo = self.field("foo", foo)
        self.bar = self.field("bar", bar)


class TestModel(object):
    def test_attrs(self):
        foo, bar = "baz", "fro"
        model = FooModel(foo, bar)

        assert model.foo == foo
        assert model.bar == bar

    def test_name(self):
        assert FooModel.get_name() == "FooModel"

    def test_registration(self):
        assert FooModel.get_name() in database.get_worksheet_names()

    def test_id(self):
        model = FooModel("test", "post")
        assert model.id