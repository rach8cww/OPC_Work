import json
import rethinkdb as r

def extract_user(**kwargs):
    return kwargs.get("user", "admin")

def extract_host(**kwargs):
    return kwargs.get("host", "localhost")

def extract_password(**kwargs):
    return kwargs.get("password", None)

class RethinkDBConnection:
    """Create a connection to a rethinkDB database"""
    def __init__(self, **kwargs):
        print(kwargs)
        self.setup(**kwargs)

    def load_config(self, **kwargs):
        """Load a configuration file"""

        # No configuration file defined, do nothing
        if "config" not in kwargs:
            return

        # Open the file and read the config
        try:
            with open(kwargs.get("config"), "r") as fin:
                config = json.loads(fin.read())

                self.user = config["user"] or self.user
                self.host = config["host"] or self.host
                self.password = config["password"] or self.password

        except Exception as e:
            print("Failed to load rethinkDB configuration file")
            print(e)
            exit(1)

    def setup(self, **kwargs):
        """Extract kwargs to something more useful"""
        self.user = extract_user(**kwargs)
        self.host = extract_host(**kwargs)
        self.password = extract_password(**kwargs)

        self.load_config(**kwargs)
        self.create_connection()

    def create_connection(self):
        """Create a connection to rethinkDB"""
        self.__connection = r.connect(
            host=self.host,
            user=self.user,
            password=self.password
        )

        return self.__connection

    def runQuery(self, query):
        """Run {query} on the current RethinkDB connection"""
        return query.run(self.__connection)
