import os

from butterdb import GDocsConnection

BUTTERDB_EMAIL = os.environ['BUTTERDB_EMAIL']
BUTTERDB_PASSWORD = os.environ['BUTTERDB_PASSWORD']

def test_oauth_connection():
    connection = GDocsConnection(BUTTERDB_EMAIL, BUTTERDB_PASSWORD)

    assert connection is not None
