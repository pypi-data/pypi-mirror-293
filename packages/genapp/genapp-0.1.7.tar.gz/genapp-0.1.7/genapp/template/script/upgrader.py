import os
import shutil
import pkg_resources


def upgrade_framework():
    # Ruta a la instalación del framework
    framework_root = pkg_resources.resource_filename("genapp", "")

    # Directorio del proyecto donde se deben actualizar los archivos
    project_root = os.getcwd()

    # Definir los directorios a actualizar
    directories_to_update = [
        "app/crud/schema",
        "app/database/connection",
        "app/database/listener",
        "app/external_api/connection",
        "app/external_api/firebase",
        "app/external_api/gmail",
        "app/lib/sqlacodegen_v2",
        "app/model",
        "app/module/smtp",
        "app/module/telegram",
        "app/module/whatsapp",
        "app/resource/public/css",
        "app/resource/public/ico",
        "app/resource/public/icons",
        "app/resource/public/img",
        "app/resource/public/js",
        "app/resource/template/email",
        "app/resource/view",
        "app/service/middleware/audit",
        "app/service/middleware/auth",
        "app/service/middleware/notification/vector",
        "app/service/request/funtionality",
        "app/service/request/sys",
        "app/service/request/web",
        "app/service/response",
        "app/util",
        "script/deploy",
        "script/generator/schemas",
        "script/migrate",
    ]

    for directory in directories_to_update:
        src = os.path.join(framework_root, directory)
        dst = os.path.join(project_root, directory)

        # Eliminar el directorio de destino si existe
        if os.path.exists(dst):
            shutil.rmtree(dst)

        # Copiar el directorio del framework al proyecto
        if os.path.exists(src):
            shutil.copytree(src, dst, dirs_exist_ok=True)
            print(f"Updated {directory}")
        else:
            print(f"Source directory {src} does not exist")

    print("Framework updated successfully!")


def main():
    upgrade_framework()


if __name__ == "__main__":
    main()
