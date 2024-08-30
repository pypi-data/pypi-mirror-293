from typing import List
from urllib.parse import parse_qs
import secure

from fastapi.staticfiles import StaticFiles
from fastapi import Depends, FastAPI, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.service.request.sys.token import Token
from app.service import request_handler as RequestHandler
from app.service.middleware.decorator import auth
from app.service.middleware.middleware import SecurityMiddleware
from starlette.responses import RedirectResponse


app = FastAPI()

# EN PRODUCCION
# app = FastAPI(docs_url=None, redoc_url=None)

oauth2_scheme = OAuth2PasswordBearer("/token", auto_error=False)
secure_headers = secure.Secure()

app.mount("/public", StaticFiles(directory="app/resource/public"), name="public")

app.add_middleware(SecurityMiddleware, secure_headers=secure_headers)


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return RedirectResponse(url="/public/ico/window2.ico")


######################################################################
################################ LOGIN ###############################
######################################################################
@app.post("/token")
async def get_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    return await Token().login(form_data, request)


@app.post("/web_token")
async def login_for_access_token(
    request: Request, form_data: OAuth2PasswordRequestForm = Depends()
):
    return await Token().login_web(form_data, request)


@app.post("/{segment_1}/{segment_2}/{segment_3}/{segment_4}")
async def run_crud_funtionality(
    request: Request,
    segment_1: str,
    segment_2: str,
    segment_3: str,
    segment_4: str,
    body: dict,
    token: str = Depends(oauth2_scheme),
):
    return await RequestHandler.crud(
        request=request,
        token=token,
        segment_1=segment_1,
        segment_2=segment_2,
        segment_3=segment_3,
        segment_4=segment_4,
        content=body,
    )


@app.post("/{segment_1}")
async def run_funtionality_post(
    request: Request, segment_1: str, body: dict, token: str = Depends(oauth2_scheme)
):
    return await RequestHandler.funtionality_POST(
        request=request, token=token, segment_1=segment_1, content=body
    )


@app.get("/{segment_1}")
async def run_funtionality_get(
    request: Request,
    segment_1: str,
    q: str = None,
    token: str = Depends(oauth2_scheme),
):
    return await RequestHandler.funtionality_GET(
        request=request,
        token=token,
        segment_1=segment_1,
        content=parse_qs(q),  # atributo1=0&atributo2=EJEMPLO2&...
    )


@app.post("/{segment_1}/{segment_2}")
async def run_funtionality_complex_post(
    request: Request,
    segment_1: str,
    segment_2: str,
    body: dict,
    token: str = Depends(oauth2_scheme),
):
    return await RequestHandler.funtionality_complex_POST(
        request=request,
        token=token,
        segment_1=segment_1,
        segment_2=segment_2,
        content=body,
    )


@app.get("/{segment_1}/{segment_2}")
async def run_funtionality_complex_get(
    request: Request,
    segment_1: str,
    segment_2: str,
    q: str = None,
    token: str = Depends(oauth2_scheme),
):
    return await RequestHandler.funtionality_complex_GET(
        request=request,
        token=token,
        segment_1=segment_1,
        segment_2=segment_2,
        content=parse_qs(q),  # atributo1=0&atributo2=EJEMPLO2&...
    )


@app.get("/{segment_1}/{path:path}")
async def run_proxy_api_get(
    request: Request, segment_1: str, path: str, token: str = Depends(oauth2_scheme)
):
    return await RequestHandler.proxy_api_GET(
        request=request, token=token, segment_1=segment_1, path=path
    )


@app.post("/{segment_1}/{path:path}")
async def run_proxy_api_post(
    request: Request,
    segment_1: str,
    path: str,
    body: dict,
    token: str = Depends(oauth2_scheme),
):
    return await RequestHandler.proxy_api_POST(
        request=request, token=token, segment_1=segment_1, path=path, content=body
    )
