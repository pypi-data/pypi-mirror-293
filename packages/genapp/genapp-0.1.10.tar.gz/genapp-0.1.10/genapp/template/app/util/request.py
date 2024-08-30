import re

from fastapi import Request


def get_ip(request: Request) -> str:
    try:
        if isinstance(request, Request):
            return str(request.headers.get("x-forwarded-for", request.client.host))

    except Exception as e:
        print("ERROR Util request -> get_ip: " + str(e))

    return None


def get_headers(request: Request) -> dict:
    try:
        if isinstance(request, Request):
            return request.headers

    except Exception as e:
        print("ERROR Util request -> get_headers: " + str(e))

    return None


def get_token_from_cookie(request: Request):
    try:
        if isinstance(request, Request):
            return request.cookies.get("access_token", None)

    except Exception as e:
        print("ERROR Util request -> get_token_from_cookie: " + str(e))

    return None


def get_clean_headers(request: Request) -> dict:
    try:
        if isinstance(request, Request):
            less_valuable_headers = [
                "host",
                "accept",
                "referer",
                "cache-control",
                "upgrade-insecure-requests",
                "connection",
                "content-length",
                "sec-ch-ua",
                "dnt",
                "sec-ch-ua-mobile",
                "sec-ch-ua-platform",
                "origin",
                "sec-fetch-site",
                "sec-fetch-user",
                "sec-fetch-mode",
                "sec-fetch-dest",
                "accept-encoding",
            ]

            filtered_headers = {
                key: value
                for key, value in request.headers.items()
                if key not in less_valuable_headers
            }
            return filtered_headers

    except Exception as e:
        print("ERROR Util request -> get_clean_headers: " + str(e))

    return None


async def get_body(request: Request) -> dict:
    try:
        if isinstance(request, Request):
            content_type = request.headers.get("content-type", "")
            if "application/json" in content_type:
                return await request.json()

    except Exception as e:
        print("ERROR Util request -> get_body: " + str(e))
    return None


def get_params(request: Request) -> str:
    try:
        if isinstance(request, Request):
            return str(request.query_params)

    except Exception as e:
        print("ERROR Util request -> get_params: " + str(e))

    return None


def get_method(request: Request) -> str:
    try:
        if isinstance(request, Request):
            return str(request.method)

    except Exception as e:
        print("ERROR Util request -> get_method: " + str(e))

    return None


def get_url(request: Request, complete=False) -> str:
    try:
        if isinstance(request, Request):
            if not complete:
                pattern = re.search(r"(.+?)(?=\?.+=)", str(request.url))

                if pattern:
                    url = pattern.group(1)
                    return str(url)

            return str(request.url)

    except Exception as e:
        print("ERROR Util request -> get_url: " + str(e))

    return None


def get_authorization_token(request: Request) -> str:
    try:
        if isinstance(request, Request):
            authorization_header = request.headers.get("authorization")

            if authorization_header:
                # Dividir el token de autorización en partes (Bearer <token>)
                token_parts = authorization_header.split()

                # Verificar si el token tiene el formato correcto
                if len(token_parts) == 2 and token_parts[0].lower() == "bearer":
                    # Retornar solo el token
                    return str(token_parts[1])

    except Exception as e:
        print("ERROR Util request -> get_authorization_token: " + str(e))

    return None
