import os

from app.database.connection.connection_postgres import PostgresDB


class GenericAppDB(PostgresDB):

    def __init__(self):
        self.username = os.getenv("API_DATABASE_USER")
        self.passwd = os.getenv("API_DATABASE_PASSWORD")
        self.host = os.getenv("API_DATABASE_HOST")
        self.port = int(os.getenv("API_DATABASE_PORT", "5432"))
        self.dbName = os.getenv("API_DATABASE_DB")
