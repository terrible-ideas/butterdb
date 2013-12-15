import fuckitdb
import os

email = os.environ["FUCKITDB_EMAIL"]
password = os.environ["FUCKITDB_PASSWORD"]


class TestDB(object):

    def test_open(self):
        """Tests opening a Database"""
        database = create_test_db()

        assert database is not None


def create_test_db():
    database = fuckitdb.Database(name="TestDB",
                                 username=email,
                                 password=password)

    return database
