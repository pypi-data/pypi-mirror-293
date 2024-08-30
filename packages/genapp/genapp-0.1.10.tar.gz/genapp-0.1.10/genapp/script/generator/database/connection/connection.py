from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker

from genapp.script.util import asynchrony as Async


class Connection:
    # Para sesiones SQLAlchemy
    session = None
    engine = None

    # Para conexiones fuera de SQLAlchemy
    connection = None

    def query_no_orm(self, query, params=None):
        try:
            if not self.connection:
                self.connect()

            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            columns = [col[0] for col in cursor.description]
            results = cursor.fetchall()
            cursor.close()

            self.disconnect()

            return [dict(zip(columns, row)) for row in results]
        except Exception as e:
            print("ERROR: Connection -> query_no_orm: " + str(e))

        return None

    def execute_no_orm(self, command, params=None):
        try:
            if not self.connection:
                self.connect()
            cursor = self.connection.cursor()
            if params:
                cursor.execute(command, params)
            else:
                cursor.execute(command)

            self.connection.commit()
            cursor.close()
            self.disconnect()

            return True
        except Exception as e:
            print("ERROR: Connection -> execute_no_orm: " + str(e))

        return False

    ################################################################
    ######################### SQLAlchemy ###########################
    ################################################################
    def newConn(self, generator=False):
        try:
            if generator:
                self.driver = self.driver_generator
            return (
                str(self.driver)
                + "://"
                + str(self.username)
                + ":"
                + str(self.passwd)
                + "@"
                + str(self.host)
                + ":"
                + str(self.port)
                + "/"
                + str(self.db_name)
            )

        except Exception as e:
            print("ERROR: Connection -> new_conn: " + str(e))

        return None

    def __enter__(self):
        self.session = self._create_session()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.session.close()
        self.session = None

    def _create_session(self):
        self.engine = create_engine(self.newConn())
        session_maker = sessionmaker(bind=self.engine, expire_on_commit=False)
        return session_maker()

    async def __aenter__(self):
        self.session = await self._create_async_session()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.session:
            await self.session.close()
            self.session = None

        if self.engine:
            await self.engine.dispose()
            self.engine = None

    async def _create_async_session(self):
        try:
            self.engine = create_async_engine(self.newConn())
            async_session_maker = async_sessionmaker(
                self.engine, expire_on_commit=False
            )
            return async_session_maker()

        except Exception as e:
            print("ERROR: Connection -> create_async_session: " + str(e))

    ##################################
    # Operaciones NATIVAS ASINCRONAS #
    ##################################
    async def async_query(self, stmt):
        try:
            async with self.session.begin():
                return await self.session.execute(stmt)
        except Exception as e:
            print("ERROR: Connection -> async_query: " + str(e))
            return e

    async def async_get(self, element, ident):
        try:
            async with self.session.begin():
                result =  await self.session.get(element, ident)
                print(result)
                return result
        except Exception as e:
            print("ERROR: Connection -> async_get: " + str(e))
            return e

    async def async_insert(self, element):
        try:
            async with self.session.begin():
                self.session.add(element)
                return element
        except Exception as e:
            print("ERROR: Connetion -> async_insert: " + str(e))
            return e

    async def async_merge(self, element):
        try:
            async with self.session.begin():
                await self.session.merge(element)
        except Exception as e:
            print("ERROR: Connetion -> async_merge: " + str(e))
            return e

        return element

    async def async_delete(self, element):
        try:
            async with self.session.begin():
                await self.session.delete(element)
                return True
        except Exception as e:
            print("ERROR: Connetion -> async_delete: " + str(e))
            return e

    #################################################################################
    # Operaciones NATIVAS NO ASINCRONAS -> SINCRONAS CONVERTIDAS MEDIANTE THREADING #
    #################################################################################
    # Convierte una tarea sincrona a asincrona, para bases de datos que no permiten asincronia
    async def _async_execute(self, callback, *args):
        try:
            return await Async.async_execute(callback, *args)

        except Exception as e:
            print("ERROR: Connetion -> async_execute: " + str(e))
            return e

    def _execute_stmt(self, stmt):
        with self.session.begin():
            return self.session.execute(stmt)

    def _execute_get(self, element, ident):
        with self.session.begin():
            return self.session.get(element, ident)

    def _execute_add(self, element):
        with self.session.begin():
            self.session.add(element)
            # self.session.flush()
            return element
            return True

    def _execute_merge(self, element):
        with self.session.begin():
            self.session.merge(element)
            return element

    def _execute_delete(self, element):
        with self.session.begin():
            self.session.delete(element)
            return True
