import os
import re
import shutil
import click
import pkg_resources

from genapp.script.generator_ import generate_model, generate_system
from genapp.script.generator.database.oracle import OracleSQLInstance
from genapp.script.generator.database.postgresql import PostgresSQLInstance
from genapp.script.generator.database.sqlserver import SQLServerInstance
from dotenv import load_dotenv

# Define la estructura de directorios base
BASE_STRUCTURE = {".": "."}


def text_to_pascal(text: str) -> str:
    try:
        words = re.split(r"(?<=[a-z])(?=[A-Z])|_", text)
        pascal_case_str = "".join(
            word.capitalize() if word.islower() else word.title() for word in words
        )
        return pascal_case_str

    except Exception as e:
        print("ERROR Util string -> text_to_pascal: " + str(e))


def copy_files(src, dst):
    """Copia los archivos de una estructura base al destino"""
    for foldername, _, filenames in os.walk(src):
        for filename in filenames:
            src_file = os.path.join(foldername, filename)
            # Construir la ruta correspondiente en el nuevo proyecto
            relative_path = os.path.relpath(src_file, src)
            dst_file = os.path.join(dst, relative_path)
            dst_folder = os.path.dirname(dst_file)

            # Asegurarse de que el directorio de destino exista
            os.makedirs(dst_folder, exist_ok=True)
            shutil.copy2(src_file, dst_file)


@click.group()
def cli():
    """CLI para gestionar la creación y actualización de proyectos GenAPP"""
    pass


@cli.command()
@click.argument("project_name")
def new(project_name):
    """Genera una nueva estructura de proyecto con archivos base"""
    if os.path.exists(project_name):
        click.echo(f"El directorio '{project_name}' ya existe.")
        return

    os.makedirs(project_name)

    # Copiar archivos base desde la carpeta de plantillas
    for folder in BASE_STRUCTURE.keys():
        for subfolder in BASE_STRUCTURE[folder]:
            subfolder_path = os.path.join(project_name, folder, subfolder)
            template_folder = pkg_resources.resource_filename(
                "genapp.template", f"{folder}/{subfolder}"
            )
            if os.path.exists(template_folder):
                copy_files(template_folder, subfolder_path)
            else:
                click.echo(
                    f"No se encontraron archivos de plantilla en: {template_folder}"
                )

    click.echo(f"Estructura del proyecto '{project_name}' creada exitosamente.")


@cli.command()
@click.argument("project_name")
def upgrade(project_name):
    """Actualiza un proyecto existente con los archivos base"""
    if not os.path.exists(project_name):
        click.echo(f"El directorio '{project_name}' no existe.")
        return

    # Copiar archivos base desde la carpeta de plantillas
    for folder in BASE_STRUCTURE.keys():
        for subfolder in BASE_STRUCTURE[folder]:
            subfolder_path = os.path.join(project_name, folder, subfolder)
            template_folder = pkg_resources.resource_filename(
                "genapp.template", f"{folder}/{subfolder}"
            )
            if os.path.exists(template_folder):
                copy_files(template_folder, subfolder_path)
            else:
                click.echo(
                    f"No se encontraron archivos de plantilla en: {template_folder}"
                )
                
    generate_system(project_name, os.getenv("API_DATABASE_NAME_CONN"))

    click.echo(f"El proyecto '{project_name}' se ha actualizado exitosamente.")


def instance_main_database():
    type = os.getenv("API_DATABASE_TYPE")
    username = os.getenv("API_DATABASE_USER")
    passwd = os.getenv("API_DATABASE_PASSWORD")
    host = os.getenv("API_DATABASE_HOST")
    port = int(os.getenv("API_DATABASE_PORT"))
    db_name = os.getenv("API_DATABASE_DB")
    db_alias = os.getenv("API_DATABASE_NAME_CONN")
    
    db_instance = None

    if type == "PostgreSQL":
        db_instance = PostgresSQLInstance(
            username, passwd, host, port, db_name, db_alias
        )

    elif type == "OracleSQL":
        db_instance = OracleSQLInstance(username, passwd, host, port, db_name, db_alias)

    elif type == "SQLServer":
        db_instance = SQLServerInstance(username, passwd, host, port, db_name, db_alias)
        
    return db_instance

@cli.command()
@click.argument("project_name", required=False)
def update_model(project_name):
    """Crea un archivo .env para conectar una base de datos"""

    if not project_name:
        project_name = os.getcwd()

    if not os.path.exists(project_name):
        click.echo(f"El directorio '{project_name}' no existe.")
        return

    env_file = os.path.join(project_name, ".env.production")
    load_dotenv(env_file)

    db_instance = instance_main_database()
    
    if db_instance:
        generate_model(
            db_instance, project_name, overwrite_model=True, overwrite_schema=True
        )


@cli.command()
@click.argument("project_name", required=False)
def set_database(project_name):
    """Crea un archivo .env para conectar la base de datos principal"""

    if not project_name:
        project_name = os.getcwd()

    if not os.path.exists(project_name):
        click.echo(f"El directorio '{project_name}' no existe.")
        return
    
    # Ruta del archivo .env
    env_path = os.path.join(project_name, ".env")
    env_production_path = os.path.join(project_name, ".env.production")

    # Verificar si ya existe un archivo .env.production
    if os.path.exists(env_production_path):
        load_existing = click.confirm(
            f"El archivo '.env.production' ya existe en '{project_name}'. ¿Deseas cargar el fichero existente?",
            default=True
        )
        if load_existing:
            load_dotenv(env_production_path)
        else:
            click.echo("Se procederá a sobrescribir el archivo '.env.production'.")
    else:
        load_existing = False

    
    if not load_existing:
        # Solicitar al usuario las variables de entorno
        db_user = click.prompt(
            "Introduce el usuario de la base de datos principal", type=str
        )
        db_password = click.prompt(
            "Introduce la contraseña de la base de datos principal", type=str
        )
        db_host = click.prompt("Introduce el host de la base de datos principal", type=str)
        db_port = click.prompt(
            "Introduce el puerto de la base de datos principal", type=str
        )
        db_name = click.prompt(
            "Introduce el nombre de la base de datos principal", type=str
        )
        db_alias = click.prompt(
            "Introduce el nombre de fichero para la base de datos principal", type=str
        )

        # Selección del tipo de base de datos
        db_type_options = {"1": "OracleSQL", "2": "PostgreSQL", "3": "SQLServer"}

        click.echo("Selecciona el tipo de base de datos:")
        for key, value in db_type_options.items():
            click.echo(f"{key}: {value}")

        db_type_choice = click.prompt(
            "Introduce el número correspondiente al tipo de base de datos",
            type=click.Choice(["1", "2", "3"]),
        )
        db_type = db_type_options[db_type_choice]
        
        
        # Escribir las variables en el archivo .env
        with open(env_path, "w") as env_file:
            env_file.write(
                "###########################################\n"
                "#      .env for production enviroment     #\n"
                "# Add more environment variables below... #\n"
                "###########################################\n\n"
            )
            env_file.write(f"API_DATABASE_USER={db_user}\n")
            env_file.write(f"API_DATABASE_PASSWORD={db_password}\n")
            env_file.write(f"API_DATABASE_HOST=172.17.0.1\n")
            env_file.write(f"API_DATABASE_PORT={db_port}\n")
            env_file.write(f"API_DATABASE_DB={db_name}\n")

        is_gen_tables = click.confirm("¿Los nombres de las tablas estructurales son los genéricos?", default=True)
    
        # Escribir las variables en el archivo .env.production
        with open(env_production_path, "w") as env_file:
            env_file.write(
                "###########################################\n"
                "#  .env.production to connect production  #\n"
                "#          environment from local         #\n"
                "#                                         #\n"
                "# Add more environment variables below... #\n"
                "###########################################\n\n"
            )
        
            env_file.write(f"API_DATABASE_USER={db_user}\n")
            env_file.write(f"API_DATABASE_PASSWORD={db_password}\n")
            env_file.write(f"API_DATABASE_HOST={db_host}\n")
            env_file.write(f"API_DATABASE_PORT={db_port}\n")
            env_file.write(f"API_DATABASE_DB={db_name}\n")
            env_file.write(f"API_DATABASE_TYPE={db_type}\n")
            env_file.write(f"API_DATABASE_NAME_CONN={db_alias}\n")
        
            # Añadir las variables adicionales al archivo .env.production
            env_file.write("\n# Name of the API structural tables in DB\n")

            if is_gen_tables:
                env_file.write("API_FUNTIONALITY=funtionality\n")
                env_file.write("API_ROLE=role\n")
                env_file.write("API_USER=user\n")
                env_file.write("API_PERMISSION=permission\n")
                env_file.write("API_AUDIT_REQUEST=audit_request\n")
                env_file.write("API_AUDIT_RESPONSE=audit_response\n")
                env_file.write("API_AUDIT_PAYLOAD=audit_payload\n")
                env_file.write("API_AUDIT_REQUEST_NOT_LOGGED=audit_request_not_logged\n")
                env_file.write("API_SCOPE=scope\n")
                env_file.write("API_CONNECTION=connection\n")
                env_file.write("API_LOGIN=login\n")
                env_file.write("API_FUNTIONALITY_PERMISSION=funtionality_need_permission\n")
                env_file.write("API_FUNTIONALITY_ATT_ID=id\n")
                env_file.write("API_ROLE_PERMISSION=role_has_permission\n")
                env_file.write("API_ROLE_SCOPE=role_has_scope\n")
                env_file.write("API_USER_PERMISSION=user_has_permission\n")
                env_file.write("API_USER_SCOPE=user_has_scope\n")
            else:
                env_file.write(f"API_FUNTIONALITY={click.prompt('Introduce el nombre de la tabla de funcionalidades', type=str)}\n")
                env_file.write(f"API_ROLE={click.prompt('Introduce el nombre de la tabla de roles', type=str)}\n")
                env_file.write(f"API_USER={click.prompt('Introduce el nombre de la tabla de usuarios', type=str)}\n")
                env_file.write(f"API_PERMISSION={click.prompt('Introduce el nombre de la tabla de permisos', type=str)}\n")
                env_file.write(f"API_AUDIT_REQUEST={click.prompt('Introduce el nombre de la tabla de auditoría de peticiones', type=str)}\n")
                env_file.write(f"API_AUDIT_RESPONSE={click.prompt('Introduce el nombre de la tabla de auditoría de respuestas', type=str)}\n")
                env_file.write(f"API_AUDIT_PAYLOAD={click.prompt('Introduce el nombre de la tabla de auditoría de payloads', type=str)}\n")
                env_file.write(f"API_AUDIT_REQUEST_NOT_LOGGED={click.prompt('Introduce el nombre de la tabla de peticiones no registradas', type=str)}\n")
                env_file.write(f"API_SCOPE={click.prompt('Introduce el nombre de la tabla de ámbitos', type=str)}\n")
                env_file.write(f"API_CONNECTION={click.prompt('Introduce el nombre de la tabla de conexion', type=str)}\n")
                env_file.write(f"API_LOGIN={click.prompt('Introduce el nombre de la tabla de login', type=str)}\n")
                env_file.write(f"API_FUNTIONALITY_PERMISSION={click.prompt('Introduce el nombre de la tabla de permisos de funcionalidades', type=str)}\n")
                env_file.write(f"API_FUNTIONALITY_ATT_ID={click.prompt('Introduce el nombre del atributo ID de la funcionalidad', type=str)}\n")
                env_file.write(f"API_ROLE_PERMISSION={click.prompt('Introduce el nombre de la tabla de permisos de roles', type=str)}\n")
                env_file.write(f"API_ROLE_SCOPE={click.prompt('Introduce el nombre de la tabla de alcance de roles', type=str)}\n")
                env_file.write(f"API_USER_PERMISSION={click.prompt('Introduce el nombre de la tabla de permisos de usuarios', type=str)}\n")
                env_file.write(f"API_USER_SCOPE={click.prompt('Introduce el nombre de la tabla de alcance de usuarios', type=str)}\n")

        # Crear el archivo CRUD en app/crud
        crud_dir = os.path.join(project_name, "app", "database")
        os.makedirs(crud_dir, exist_ok=True)
        crud_file_path = os.path.join(crud_dir, f"{db_alias}.py")

        db_conn_type = {
            "1": ("connection_oracle", "OracleDB"),
            "2": ("connection_postgres", "PostgresDB"),
            "3": ("connection_microsoft", "SQLServerDB"),
        }

        conn_file_name, conn_class_name = db_conn_type[db_type_choice]

        with open(crud_file_path, "w") as crud_file:
            crud_file.write(
                f"from app.database.connection.{conn_file_name} import {conn_class_name}\n"
                f"import os\n\n\n"
                f"class {text_to_pascal(db_alias)}({conn_class_name}):\n\n"
                f"    def __init__(self):\n"
                f"        self.username = os.getenv('API_DATABASE_USER')\n"
                f"        self.passwd = os.getenv('API_DATABASE_PASSWORD')\n"
                f"        self.host = os.getenv('API_DATABASE_HOST')\n"
                f"        self.port = int(os.getenv('API_DATABASE_PORT', '{db_port}'))\n"
                f"        self.db_name = os.getenv('API_DATABASE_DB')\n"
            )

        click.echo(f"Archivo .env creado exitosamente en '{env_path}'")
        click.echo(f"Archivo CRUD creado exitosamente en '{crud_file_path}'")

        load_dotenv(env_production_path)
        
    
    db_instance = instance_main_database()
    
    if db_instance:
        generate_model(
            db_instance, project_name, overwrite_model=True, overwrite_schema=True
        )

    generate_system(project_name, db_instance.alias)

cli()
