import asyncio
from concurrent.futures import ThreadPoolExecutor

import cx_Oracle

from app.database.connection.connection import Connection


class OracleDB(Connection):
    driver = "oracle+cx_oracle"
    driver_generator = "oracle+cx_oracle"
    mandatory_order = False

    def connect(self):
        try:
            dsn = cx_Oracle.makedsn(self.host, self.port, self.dbName)
            self.connection = cx_Oracle.connect(
                self.username, self.passwd, dsn)

        except Exception as e:
            print("ERROR: Connetion oracle -> connect: " + str(e))

    def disconnect(self):
        try:
            if self.connection:
                self.connection.close()
                self.connection = None
        except Exception as e:
            print("ERROR: Connetion oracle -> disconnect: " + str(e))

    ############################################
    # Operaciones NATIVAS ASINCRONAS OVERWRITE #
    ############################################
    async def async_query(self, stmt):
        try:
            return await self._async_execute(self._execute_stmt, stmt)
        except Exception as e:
            print("ERROR: Connetion oracle -> async_query: " + str(e))
            return e

    async def async_get(self, element, ident):
        try:
            return await self._async_execute(self._execute_get, element, ident)
        except Exception as e:
            print("ERROR: Connection oracle -> async_get: " + str(e))
            return e

    async def async_insert(self, element):
        try:
            return await self._async_execute(self._execute_add, element)
        except Exception as e:
            print("ERROR: Connetion oracle -> async_insert: " + str(e))
            return e

    async def async_merge(self, element):
        try:
            return await self._async_execute(self._execute_merge, element)
        except Exception as e:
            print("ERROR: Connetion oracle -> async_merge: " + str(e))
            return e

    async def async_delete(self, element):
        try:
            return await self._async_execute(self._execute_delete, element)
        except Exception as e:
            print("ERROR: Connetion oracle -> async_delete: " + str(e))
            return e

    #####################################################################
    # OVERWRITE PROTOCOLO DE ENTRADA Y SALIDA PARA FUNCIONES ASINCRONAS #
    #####################################################################

    async def __aenter__(self):
        self.session = self._create_session()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.session:
            self.session.close()
            self.session = None

        if self.engine:
            self.engine.dispose(close=True)
            self.engine = None
