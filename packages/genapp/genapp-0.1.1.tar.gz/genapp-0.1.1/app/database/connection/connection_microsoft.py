import pyodbc

from app.database.connection.connection import Connection


class SQLServerDB(Connection):
    driver = "mssql+aioodbc"
    driver_generator = "mssql+pyodbc"
    mandatory_order = True

    def connect(self):
        try:
            conn_str = (
                f"DRIVER={{ODBC Driver 18 for SQL Server}};"
                f"SERVER={self.host};"
                f"DATABASE={self.dbName};"
                f"UID={self.username};"
                f"PWD={self.passwd};"
                f"Encrypt=yes;"
                f"TrustServerCertificate=yes;"
            )
            self.connection = pyodbc.connect(conn_str)
        except Exception as e:
            print("ERROR: Connetion microsoft -> connect: " + str(e))

    def disconnect(self):
        try:
            if self.connection:
                self.connection.close()
                self.connection = None
        except Exception as e:
            print("ERROR: Connetion microsoft -> disconnect: " + str(e))

    def newConn(self, generator=False):
        try:
            return (
                super().newConn(generator=generator)
                + "?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=yes"
            )
        except Exception as e:
            print("ERROR: Connetion microsoft -> newConn: " + str(e))

    # Convierte una tarea sincrona a asincrona, para bases de datos que no permiten asincronia
    # async def async_execute(self, stmt):
    #     try:
    #         loop = asyncio.get_event_loop()
    #         with ThreadPoolExecutor(max_workers=1) as executor:
    #             result = await loop.run_in_executor(executor, self._execute_stmt, stmt)
    #             return result
    #     except Exception as e:
    #         print("ERROR: Connetion microsoft -> async_execute: " + str(e))
    #         return None

    # def _execute_stmt(self, stmt):
    #     try:
    #         return self.session.execute(stmt)
    #     except Exception as e:
    #         print("ERROR: Connetion microsoft -> execute_stmt: " + str(e))
    #         return e

    # async def __aenter__(self):
    #     self.session = self._create_session()
    #     return self

    # async def __aexit__(self, exc_type, exc, tb):
    #     self.session.close()
