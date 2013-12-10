import fuckitdb
import test_database

database = test_database.create_test_db()

@database.register()
class FooModel(fuckitdb.Model):
    def __init__(self, foo, bar):
        self.foo = foo
        self.bar = bar
        self.register(database)


class TestModel(object):
    def test_attrs(self):
        foo, bar = "baz", "fro"
        model = FooModel(foo, bar)

        assert model.foo == foo
        assert model.bar == bar


