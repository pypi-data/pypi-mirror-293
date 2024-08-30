###############################################################
###################### (NO MODIFICABLES) ######################
###############################################################

# Claves de los esquemas para ser sustituidos

# Keys que sustituyen a nombres de directorios
CRUD_KEY = "CRUD_KEY"
MODEL_KEY = "MODEL_KEY"
DATABASE_KEY = "DATABASE_KEY"
SCHEMA_KEY = "SCHEMA_KEY"
SERVICE_KEY = "SERVICE_KEY"
CONTROLLER_KEY = "CONTROLLER_KEY"

# Keys que sustituyen a nombre de variables
DATABASE_NAME_KEY = "DATABASE_NAME_KEY"  # Nombre de la bbdd
DATABASE_CLASS_KEY = "DATABASE_CLASS_KEY"  # Nombre de la bbdd en PascalCase

# Nombre del esquema SQL Alchemy generado
SCHEMA_DATABASE_KEY = "SCHEMA_DATABASE_KEY"
FILE_NAME_KEY = "FILE_NAME_KEY"  # Nombre de una tabla en bbdd en snake_case

CLASS_NAME_KEY = "CLASS_NAME_KEY"  # Nombre de una tabla en PascalCase

# Nombre de la tabla funtionality en la bbdd principal en snake_case
API_FUNTIONALITY_KEY = "API_FUNTIONALITY_KEY"
API_FUNTIONALITY_CLASS_KEY = "API_FUNTIONALITY_CLASS_KEY"

# Nombre de la tabla role en la bbdd principal en snake_case
API_ROLE_KEY = "API_ROLE_KEY"
# Nombre de la tabla role en la bbdd principal en PascalCase
API_ROLE_CLASS_KEY = "API_ROLE_CLASS_KEY"

# Nombre de la tabla audit_request en la bbdd principal en snake_case
API_AUDIT_REQUEST_KEY = "API_AUDIT_REQUEST_KEY"
# Nombre de la tabla audit_request en la bbdd principal en PascalCase
API_AUDIT_REQUEST_CLASS_KEY = "API_AUDIT_REQUEST_CLASS_KEY"
# Nombre de la tabla audit_response en la bbdd principal en snake_case
API_AUDIT_RESPONSE_KEY = "API_AUDIT_RESPONSE_KEY"
# Nombre de la tabla audit_response en la bbdd principal en PascalCase
API_AUDIT_RESPONSE_CLASS_KEY = "API_AUDIT_RESPONSE_CLASS_KEY"

# Nombre de la tabla audit_payload en la bbdd principal en snake_case
API_AUDIT_PAYLOAD_KEY = "API_AUDIT_PAYLOAD_KEY"
# Nombre de la tabla audit_payload en la bbdd principal en PascalCase
API_AUDIT_PAYLOAD_CLASS_KEY = "API_AUDIT_PAYLOAD_CLASS_KEY"


# Nombre de la tabla connection en la bbdd principal en snake_case
API_CONNECTION_KEY = "API_CONNECTION_KEY"
# Nombre de la tabla connection en la bbdd principal en PascalCase
API_CONNECTION_CLASS_KEY = "API_CONNECTION_CLASS_KEY"


API_AUDIT_REQUEST_NOT_LOGGED_CLASS_KEY = "API_AUDIT_REQUEST_NOT_LOGGED_CLASS_KEY"
API_AUDIT_REQUEST_NOT_LOGGED_KEY = "API_AUDIT_REQUEST_NOT_LOGGED_KEY"

# Nombre de la tabla login en la bbdd principal en snake_case
API_LOGIN_KEY = "API_LOGIN_KEY"
# Nombre de la tabla login en la bbdd principal en PascalCase
API_LOGIN_CLASS_KEY = "API_LOGIN_CLASS_KEY"

# Nombre de la tabla user en la bbdd principal en snake_case
API_USER_KEY = "API_USER_KEY"

# Nombre de la tabla permission en la bbdd principal en snake_case
API_PERMISSION_KEY = "API_PERMISSION_KEY"

# Nombre de la tabla funtionality_need_permission en la bbdd principal en snake_case
API_FUNTIONALITY_PERMISSION_KEY = "API_FUNTIONALITY_PERMISSION_KEY"
# Nombre de la tabla role_has_permission en la bbdd principal en snake_case
API_ROLE_PERMISSION_KEY = "API_ROLE_PERMISSION_KEY"
API_ROLE_SCOPE_KEY = (
    "API_ROLE_SCOPE_KEY"  # Nombre de la tabla role_has_scope en snake_case
)
# Nombre de la tabla user_has_permission en la bbdd principal en snake_case
API_USER_PERMISSION_KEY = "API_USER_PERMISSION_KEY"
# Nombre de la tabla user_has_scope en la bbdd principal en snake_case
API_USER_SCOPE_KEY = "API_USER_SCOPE_KEY"

API_SCOPE_CLASS_KEY = "API_SCOPE_CLASS_KEY"

# Nombres de ficheros estructurales
FILE_NAME_CACHE = "cache"
FILE_NAME_AUTH = "auth"
FILE_NAME_TOKEN = "token"
FILE_NAME_AUDIT = "audit"
FILE_NAME_CONN = "conn"
FILE_NAME_LOGIN = "login"
FILE_NAME_PAYLOAD = "payload"

# Tipos de crud contemplados en la api (NO MODIFICABLE mientras no se implementen mas en los dao)
CRUDS = ["query", "insert", "update", "delete"]

# Ruta de los esquemas necesarios para ejecutar model_generator
ROUTE_SCHEMAS_GENERATOR = "schemas"

SCHEMA_ROLE_DAO_FILE = "role_dao_file_schema"
SCHEMA_FUNTIONALITY_DAO_FILE = "funtionality_dao_file_schema"
SCHEMA_USER_DAO_FILE = "user_dao_file_schema"
SCHEMA_CACHE_FILE = "cache_file_schema"
SCHEMA_CACHE_LISTENER_FILE = "cache_listener_file_schema"
SCHEMA_AUTHORIZATION_FILE = "authorization_file_schema"
SCHEMA_TOKEN = "token_file_schema"
SCHEMA_AUDIT = "audit_file_schema"
SCHEMA_PAYLOAD = "payload_file_schema"

SCHEMA_LOGIN_DAO_FILE = "login_dao_file_schema"
SCHEMA_LOGIN_FILE = "login_file_schema"
SCHEMA_CONNECTION_DAO_FILE = "connection_dao_file_schema"
SCHEMA_CONNECTION_FILE = "conn_file_schema"


# Nombre de los directorios
APP = "app"  # Nombre del directorio donde se almacena el proyecto principal
CRUD = "crud"  # Nombre del directorio donde se guardara los Data Access Object
MODEL = "model"  # Nombre del directorio donde se guardara los DTO de pydantic organizados por cada BBDD
# Nombre del directorio donde se guardara los esquemas de BBDD de SQLAlchemy
SCHEMA = "schema"
# Nombre del directorio donde se encuentra el paquete conexion y se definen las BBDD
DATABASE = "database"
# Nombre del directorio donde se encuentra el paquete controlador y las rutas disponibles de la API
SERVICE = "service"
# Nombre del directorio donde se alamcenan todas las posibles solicitudes al sistema
REQUEST = "request"
# Nombre del directorio donde se encuentran los middleware, decoradores..
MIDDLEWARE = "middleware"
# Nombre del directorio donde se declaran los controladores propios del sistema, authorization, gestion de solicitudes..
SYS = "sys"
AUDIT = "audit"  # Nombre del directorio del middleware audit
AUTH = "auth"  # Nombre del directorio del middleware auth
