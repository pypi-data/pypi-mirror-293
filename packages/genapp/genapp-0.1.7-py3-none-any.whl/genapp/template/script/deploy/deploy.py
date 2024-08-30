import paramiko
import os


def deploy_application():
    # SSH connection settings
    ssh_host = os.getenv("SERVER_PROD_HOST")
    ssh_port = os.getenv("SERVER_PROD_PORT")
    ssh_username = os.getenv("SERVER_PROD_USERNAME")
    ssh_password = os.getenv("SERVER_PROD_PASSWD")

    # Remote directory and Docker Compose file
    remote_dir = "/home/webserv11-user/apirest_dephy"
    docker_compose_file = remote_dir + "/docker-compose.yml"

    # SSH connection
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ssh_host, port=ssh_port,
                       username=ssh_username, password=ssh_password)

    # SSH commands
    commands = [
        # Pull the latest changes from the repository
        f"git -C {remote_dir} pull origin master",
        # Stop and remove containers defined in the compose file
        f"docker-compose -f {docker_compose_file} down",
        # Build or update Docker image and deploy
        f"docker-compose -f {docker_compose_file} up -d --build",
    ]

    # Execute commands
    for command in commands:
        stdin, stdout, stderr = ssh_client.exec_command(command)
        print(stdout.read().decode())
        print(stderr.read().decode())

    # Close SSH connection
    ssh_client.close()
