from time import sleep

import psycopg2
from psycopg2 import extensions

from genapp.script.generator.database.connection.connection import Connection


class PostgresDB(Connection):
    driver = "postgresql+asyncpg"
    driver_generator = "postgresql"
    mandatory_order = False

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.dbName,
                user=self.username,
                password=self.passwd,
                port=self.port,
            )

        except Exception as e:
            print("ERROR: Connetion postgre -> connect: " + str(e))

    def disconnect(self):
        try:
            if self.connection:
                self.connection.close()
                self.connection = None
        except Exception as e:
            print("ERROR: Connetion postgre -> disconnect: " + str(e))

    def _initListener(self, channel):
        try:
            if self.connection:
                self.connection.set_isolation_level(
                    extensions.ISOLATION_LEVEL_AUTOCOMMIT
                )
                self.connection.cursor().execute(f"LISTEN {channel};")
        except Exception as e:
            print("ERROR: Connetion postgre -> initListener: " + str(e))

    # Recibe una funcion como parametro, sera la ejecutora del evento escuchado
    def listenCallbackWithPayload(self, channel, callback):
        try:
            self._initListener(channel)
            if self.connection:
                while True:
                    self.connection.poll()
                    while self.connection.notifies:
                        notification = self.connection.notifies.pop(0)
                        callback(notification.payload)
                    sleep(2)

        except Exception as e:
            print("ERROR: Connetion postgre -> listenCallbackWithPayload: " + str(e))

    def listen(self, channel, callback):
        try:
            self._initListener(channel)
            if self.connection:
                while True:
                    self.connection.poll()
                    notifications = self.connection.notifies

                    if notifications:
                        callback()
                        self.connection.notifies.clear()
                    sleep(2)

        except Exception as e:
            print("ERROR: Connetion postgre -> listen: " + str(e))

        # Ejemplo de trigger
        """
            CREATE OR REPLACE FUNCTION notify_change()
            RETURNS TRIGGER AS $$
            BEGIN
                -- Notificar sobre el cambio en la tabla
                PERFORM pg_notify('channel_funtionality_permission', 'change occurred');
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
            
            CREATE TRIGGER table_change_trigger
            AFTER INSERT OR UPDATE OR DELETE
            ON tu_tabla
            FOR EACH ROW
            EXECUTE FUNCTION notify_change();
            
        """
