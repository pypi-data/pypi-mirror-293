from genapp.script.generator.database.connection.connection import Connection
from genapp.script.generator.database.connection.connection_postgres import PostgresDB
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from . import generator_
from .migrate import api_schema


def migrate(
    database_recipient,
    database_recipient_schema="public",
    sqlAlchemy_schema=None,
    create_triggers=False,
    init_data=False,
    generate_api=False,
):
    try:
        if isinstance(database_recipient, Connection):
            conn = database_recipient.newConn()

            engine = create_engine(conn)

            if not sqlAlchemy_schema:
                sqlAlchemy_schema = api_schema

            sqlAlchemy_schema.metadata.create_all(engine)

            if init_data:
                init_api_data(sqlAlchemy_schema, engine)

            if create_triggers:
                if isinstance(database_recipient, PostgresDB):
                    create_postgres_trigger_permission(
                        database_recipient, database_recipient_schema
                    )
                    create_postgres_trigger_permission_admin(
                        database_recipient, database_recipient_schema
                    )
                    create_postgres_trigger_funtionality_need_permission(
                        database_recipient, database_recipient_schema
                    )
                else:
                    create_trigger_permission(
                        database_recipient, database_recipient_schema
                    )
                    create_trigger_permission_admin(
                        database_recipient, database_recipient_schema
                    )
                    create_trigger_functionality_need_permission(
                        database_recipient, database_recipient_schema
                    )

            if generate_api:
                generator_.generate(
                    database_recipient,
                    overwrite_model=True,
                    overwrite_dao=True,
                    update_funtionalities=True,
                )

    except Exception as e:
        print("ERROR: Migrate database -> migrate: " + str(e))


def init_api_data(sqlAlchemy_schema, engine):
    try:
        admin = sqlAlchemy_schema.Role(id=0, name="admin")
        permission_query = sqlAlchemy_schema.Permission(name="query")
        permission_insert = sqlAlchemy_schema.Permission(name="insert")
        permission_update = sqlAlchemy_schema.Permission(name="update")
        permission_delete = sqlAlchemy_schema.Permission(name="delete")

        session = sessionmaker(bind=engine)()
        session.add(admin)
        session.add(permission_query)
        session.add(permission_insert)
        session.add(permission_update)
        session.add(permission_delete)
        session.commit()

    except Exception as e:
        print("ERROR: Migrate database -> create_trigger_permission: " + str(e))


def create_trigger_permission(database_recipient, database_recipient_schema):
    try:
        database_recipient.execute(
            f"""
                CREATE TRIGGER {database_recipient_schema}.after_insert_funtionality
                AFTER INSERT ON {database_recipient_schema}.funtionality
                BEGIN
                    -- Insertar un nuevo permiso en la tabla permission con la composición concatenada de los valores de name, database, crud_type y table de la funcionalidad insertada
                    INSERT INTO {database_recipient_schema}.permission (id, name) VALUES (NEW.id, NEW.name || '_' || NEW.database || '_' || NEW.crud_type || '_' || NEW.table);
                END;
            """
        )
    except Exception as e:
        print("ERROR: Migrate database -> create_trigger_permission: " + str(e))


def create_trigger_permission_admin(database_recipient, database_recipient_schema):
    try:
        database_recipient.execute(
            f"""
                CREATE TRIGGER {database_recipient_schema}.after_insert_permission
                AFTER INSERT ON {database_recipient_schema}.permission
                BEGIN
                    -- Insertar un nuevo registro en la tabla role_has_permission con id_role = 0 y id_permission igual al new.id
                    INSERT INTO {database_recipient_schema}.role_has_permission (id_role, id_permission) VALUES (0, NEW.id);
                END;
            """
        )
    except Exception as e:
        print("ERROR: Migrate database -> create_trigger_permission_admin: " + str(e))


def create_trigger_functionality_need_permission(
    database_recipient, database_recipient_schema
):
    try:
        database_recipient.execute(
            f"""
                CREATE TRIGGER {database_recipient_schema}.after_insert_functionality_need_permission
                AFTER INSERT ON {database_recipient_schema}.funtionality
                BEGIN
                    -- Insertar un nuevo registro en la tabla funtionality_need_permission con id_funtionality igual al new.id y id_permission igual al new_.id
                    INSERT INTO {database_recipient_schema}.funtionality_need_permission (id_funtionality, id_permission) VALUES (NEW.id, NEW.id);
                    CASE
                        WHEN NEW.crud_type = 'query' THEN
                            INSERT INTO {database_recipient_schema}.funtionality_need_permission (id_funtionality, id_permission) VALUES (NEW.id, 1);
                        WHEN NEW.crud_type = 'insert' THEN
                            INSERT INTO {database_recipient_schema}.funtionality_need_permission (id_funtionality, id_permission) VALUES (NEW.id, 2);
                        WHEN NEW.crud_type = 'update' THEN
                            INSERT INTO {database_recipient_schema}.funtionality_need_permission (id_funtionality, id_permission) VALUES (NEW.id, 3);
                        WHEN NEW.crud_type = 'delete' THEN
                            INSERT INTO {database_recipient_schema}.funtionality_need_permission (id_funtionality, id_permission) VALUES (NEW.id, 4);
                    END CASE;
                END;
            """
        )

    except Exception as e:
        print(
            "ERROR: Migrate database -> create_trigger_functionality_need_permission: "
            + str(e)
        )


###############################################################
#################### TRIGGERS FOR POSTGRESQL ##################
###############################################################


def create_postgres_trigger_permission(database_recipient, database_recipient_schema):
    try:
        database_recipient.execute(
            f"""ALTER TABLE {database_recipient_schema}.funtionality ALTER COLUMN id SET DEFAULT nextval('id_funtionality_seq'::regclass);"""
        )
        database_recipient.execute(
            f"""
                CREATE OR REPLACE FUNCTION {database_recipient_schema}.before_insert_funtionality_permission()
                RETURNS TRIGGER AS $$
                BEGIN
                    -- Insertar un nuevo permiso en la tabla permission con la composición concatenada de los valores de name, database, crud_type y table de la funcionalidad insertada
                    INSERT INTO {database_recipient_schema}.permission (name) VALUES (NEW.name || '_' || NEW.database || '_' || NEW.crud_type || '_' || NEW.table);
                    RETURN NEW;
                END;
                $$ LANGUAGE plpgsql;
            """
        )

        database_recipient.execute(
            f"""
                CREATE TRIGGER trig_before_insert_funtionality_permission
                BEFORE INSERT ON {database_recipient_schema}.funtionality
                FOR EACH ROW EXECUTE FUNCTION {database_recipient_schema}.before_insert_funtionality_permission();
            """
        )
    except Exception as e:
        print(
            "ERROR: Migrate database -> create_postgres_trigger_permission: " + str(e)
        )


def create_postgres_trigger_permission_admin(
    database_recipient, database_recipient_schema
):
    try:
        database_recipient.execute(
            f"""
                CREATE OR REPLACE FUNCTION {database_recipient_schema}.after_insert_permission_admin()
                    RETURNS TRIGGER AS $$
                    BEGIN
                        -- Insertar un nuevo registro en la tabla role_has_permission con id_role = 0 y id_permission igual al new.id
                        INSERT INTO {database_recipient_schema}.role_has_permission (id_role, id_permission) VALUES (0, NEW.id);
                        RETURN NEW;
                END;
                $$ LANGUAGE plpgsql;
            """
        )

        database_recipient.execute(
            f"""
                CREATE TRIGGER trig_after_insert_permission_admin
                AFTER INSERT ON {database_recipient_schema}.permission
                FOR EACH ROW EXECUTE FUNCTION {database_recipient_schema}.after_insert_permission_admin();
            """
        )
    except Exception as e:
        print(
            "ERROR: Migrate database -> create_postgres_trigger_permission_admin: "
            + str(e)
        )


def create_postgres_trigger_funtionality_need_permission(
    database_recipient, database_recipient_schema
):
    try:
        database_recipient.execute(
            f"""
                CREATE OR REPLACE FUNCTION {database_recipient_schema}.after_insert_funtionality_need_permission()
                RETURNS TRIGGER AS $$
                BEGIN
                    -- Insertar un nuevo registro en la tabla funtionality_need_permission con id_funtionality igual al new.id y id_permission igual al máximo valor de id en la tabla permission
                    INSERT INTO {database_recipient_schema}.funtionality_need_permission (id_funtionality, id_permission) 
                    VALUES (NEW.id, (SELECT MAX(id) FROM {database_recipient_schema}.permission));
                    
                    CASE
                        WHEN NEW.crud_type = 'query' THEN
                            INSERT INTO {database_recipient_schema}.funtionality_need_permission (id_funtionality, id_permission) VALUES (NEW.id, 1);
                        WHEN NEW.crud_type = 'insert' THEN
                            INSERT INTO {database_recipient_schema}.funtionality_need_permission (id_funtionality, id_permission) VALUES (NEW.id, 2);
                        WHEN NEW.crud_type = 'update' THEN
                            INSERT INTO {database_recipient_schema}.funtionality_need_permission (id_funtionality, id_permission) VALUES (NEW.id, 3);
                        WHEN NEW.crud_type = 'delete' THEN
                            INSERT INTO {database_recipient_schema}.funtionality_need_permission (id_funtionality, id_permission) VALUES (NEW.id, 4);
                    END CASE;
                    
                    RETURN NEW;
                END;
                $$ LANGUAGE plpgsql;
            """
        )

        database_recipient.execute(
            f"""
                CREATE TRIGGER trig_after_insert_funtionality_need_permission
                AFTER INSERT ON {database_recipient_schema}.funtionality
                FOR EACH ROW EXECUTE FUNCTION {database_recipient_schema}.after_insert_funtionality_need_permission();
            """
        )

    except Exception as e:
        print(
            "ERROR: Migrate database -> create_postgres_trigger_funtionality_need_permission: "
            + str(e)
        )
