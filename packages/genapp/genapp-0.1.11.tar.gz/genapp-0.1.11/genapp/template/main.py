import argparse
import asyncio
from contextlib import asynccontextmanager

import cx_Oracle
import uvicorn
from dotenv import load_dotenv

import app.service.cache as Cache
from app.service.api import app
from app.util import path as Path
from app.util import file as File

DATABASE_PRODUCTION = "production"
DATABASE_LOCALHOST = "localhost"
DATABASE_SUPABASE = "supabase"

ENVIRONMENT_PRODUCTION = ".env.production"
ENVIRONMENT_SUPABASE = ".env.supabase"
ENVIRONMENT_DEVELOPER = ".env.dev"
ENVIRONMENT = ".env"

PATH_ORACLE = "/opt/oracle/instantclient"


# Funciones que se ejecutaran en el inicio ciclicamente
async def startup():
    asyncio.create_task(Cache.async_update_funtionality_permissions())
    asyncio.create_task(Cache.async_update_role_permissions())
    asyncio.create_task(Cache.async_update_funtionalities())
    asyncio.create_task(Cache.async_update_role_scope())
    asyncio.create_task(Cache.load_connection_data())


def main(env=None):
    root_path = Path.get_current_path()

    if env == DATABASE_PRODUCTION:
        env_file = Path.get_path_file(root_path, ENVIRONMENT_PRODUCTION)
    elif env == DATABASE_LOCALHOST:
        env_file = Path.get_path_file(root_path, ENVIRONMENT_DEVELOPER)
    elif env == DATABASE_SUPABASE:
        env_file = Path.get_path_file(root_path, ENVIRONMENT_SUPABASE)
    else:
        # .env apunta a la bbdd de la maquina host del que ejecuta el docker
        if File.exist_directory(PATH_ORACLE):
            cx_Oracle.init_oracle_client(lib_dir=PATH_ORACLE)
        env_file = Path.get_path_file(root_path, ENVIRONMENT)

    load_dotenv(env_file)

    # Se incorpora al bucle de eventos asincronos de FastApi
    app.add_event_handler("startup", startup)
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Conectado con la base de datos de producción"
    )
    parser.add_argument(
        "-d", "--database", type=str, help='Database environment (e.g., "production")'
    )

    args = parser.parse_args()
    if args.database:
        main(env=args.database)
    else:
        main()
