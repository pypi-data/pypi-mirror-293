from genapp.script.generator.database.connection.connection_microsoft import SQLServerDB


class SQLServerInstance(SQLServerDB):

    def __init__(self, username, passwd, host, port, db_name, alias):
        self.username = username
        self.passwd = passwd
        self.host = host
        self.port = port
        self.db_name = db_name
        self.alias = alias