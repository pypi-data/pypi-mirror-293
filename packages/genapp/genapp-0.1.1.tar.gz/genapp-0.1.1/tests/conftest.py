import os

from dotenv import load_dotenv


from app.util import path as Path


def pytest_addoption(parser):
    parser.addoption(
        "-D",
        "--env",
        action="store",
        help="Specify the environment for tests",
    )


def pytest_configure(config):
    env = config.getoption("env")
    if env:
        root_path = Path.get_previous_path(previous=2)
        env_file = Path.get_path_file(root_path, ".env.production")

        if os.path.exists(env_file):
            load_dotenv(env_file, override=True)
        else:
            print(f"Warning: {env_file} not found. Using default .env file.")
