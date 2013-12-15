import fuckitdb
import os

email = os.environ["FUCKITDB_EMAIL"]
password = os.environ["FUCKITDB_PASSWORD"]

db = fuckitdb.Database(name="TestDB",
                       username=email,
                       password=password)


@db.register()
class User(fuckitdb.Model):
    def __init__(self, username, email, age):
        super(User, self).__init__()
        self.username = self.field("username", username)
        self.email = self.field("email", email)
        self.age = self.field("age", age)


a = User("widdershin", "test@gmail.com", "43")
b = User("test", "fxfds@gmail.com", "12")
c = User("bvbvb", "fxfds@gdfg.com", "22222222")
