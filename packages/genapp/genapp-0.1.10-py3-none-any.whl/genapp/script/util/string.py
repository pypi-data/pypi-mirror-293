import hashlib
import random
import re
import string
from keyword import iskeyword


def text_to_class(text: str) -> str:
    try:
        # words = re.split(r"(?<=[a-z])(?=[A-Z])|_", text)
        # pascal_case_str = "".join(
        #     word.capitalize() if word.islower() else word.title() for word in words
        # )
        # return pascal_case_str

        aux = re.compile(r"(?u)\W").sub("_", text)
        aux = "".join(part[:1].upper() + part[1:] for part in aux.split("_"))
        aux = aux.strip()
        aux = re.compile(r"(?u)\W").sub("_", aux)
        if aux[0].isdigit():
            aux = "_" + aux
        elif iskeyword(aux) or aux == "metadata":
            aux += "_"

        return aux

    except Exception as e:
        print("ERROR Util string -> text_to_class: " + str(e))


def text_to_pascal(text: str) -> str:
    try:
        words = re.split(r"(?<=[a-z])(?=[A-Z])|_", text)
        pascal_case_str = "".join(
            word.capitalize() if word.islower() else word.title() for word in words
        )
        return pascal_case_str

    except Exception as e:
        print("ERROR Util string -> text_to_pascal: " + str(e))


def text_to_snake(text: str) -> str:
    try:
        snake_case_str = "_".join(
            word.lower() for word in re.split(r"(?<=[a-z])(?=[A-Z])|_", text)
        )
        return snake_case_str
    except Exception as e:
        print("ERROR Util string -> text_to_snake: " + str(e))


def get_valid_attribute(name: str) -> str:
    try:
        name += "_" if iskeyword(name) or name == "metadata" else ""
        return name
    except Exception as e:
        print("ERROR Util string -> get_valid_attribute: " + str(e))


def text_to_sha256(text: str) -> str:
    # Crear un objeto hash SHA-256
    sha256 = hashlib.sha256()
    # Convertir el string a bytes y actualizar el hash
    sha256.update(text.encode("utf-8"))
    # Obtener el valor hexadecimal del hash
    hash_256 = sha256.hexdigest()

    return hash_256


def get_module(packages: list[str]) -> str:
    try:
        if not packages:
            return ""

        path_module = ".".join(packages)
        return path_module

    except Exception as e:
        print("ERROR Util string -> get_module: " + str(e))


def random_string(length: int) -> str:
    try:
        return "".join(
            random.choice(string.ascii_lowercase + string.ascii_uppercase)
            for _ in range(length)
        )
    except Exception as e:
        print("ERROR Util string -> random_string: " + str(e))
    return None


def is_valid_sha256(hash_passwd: str) -> bool:
    try:
        if re.fullmatch(r"[a-f0-9]{64}", hash_passwd):
            return True
        return False
    except Exception as e:
        print("ERROR Util string -> is_valid_sha256: " + str(e))


def decode(bytes: bytes) -> str:
    try:
        return bytes.decode("utf-8")
    except Exception as e:
        print("ERROR Util string -> decode: " + str(e))
    return None
