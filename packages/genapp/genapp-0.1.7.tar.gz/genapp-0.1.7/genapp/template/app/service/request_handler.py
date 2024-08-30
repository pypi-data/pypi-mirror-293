from fastapi import HTTPException

from app.util import object as Obj
from app.service.middleware.decorator import audit, auth, debug
from app.service.request.request import Request, RequestKeys
from app.service.request.sys.crud import Crud
from app.service.request.sys.proxy_api import ProxyAPI

from app.service.response.response import JSONResponseAPI


USER = "user"  # Objeto Sqlalchemy User obtenido en @auth
FUNTIONALITY = "funtionality"
REQUEST = "request"

TYPE_RESPONSE_JSON = "json"
TYPE_RESPONSE_WEB = "web"

"""

   Todos los atributos de los segmentos se deben llamar  
   segment_1, segment_2, segment_3, ...
   
   Se utilizan esos nombres de atributo en @Auth para validar las funcionalidades

    
"""


# Atiende a las funcionalidades crud proporcionados por la api
@auth
@audit
async def crud(segment_1, segment_2, segment_3, segment_4, content, **kwargs):
    header, body = _get_header_body(content)
    # Interceptar body dentro de content. content = {"body": {}, "header": {}}
    result, data = await Crud(
        database=segment_2,
        crud_type=segment_3,
        table=segment_4,
        header=header,
        body=body,
    ).start()

    return JSONResponseAPI(body_header=header, result=result, data=data)


#########################################
################## API ##################
#########################################
@auth
@audit
# Atiende a funcionalidades por POST definidas por el desarrollador
async def funtionality_POST(segment_1, content, **kwargs):
    user = kwargs.get(USER, None)
    request = kwargs.get(REQUEST, None)
    funtionality = kwargs.get(FUNTIONALITY, None)

    header, body = _get_header_body(content)

    request_func = _get_request(request, funtionality, segment_1)

    if hasattr(request_func, RequestKeys.POST):
        if funtionality.type_response == TYPE_RESPONSE_JSON:
            header, result, data = await getattr(request_func, RequestKeys.POST)(
                header=header, user=user, body=body
            )

            return JSONResponseAPI(body_header=header, result=result, data=data)

        elif funtionality.type_response == TYPE_RESPONSE_WEB:
            return await getattr(request_func, RequestKeys.POST)(
                content=content, user=user
            )

    else:
        raise HTTPException(status_code=501, detail="Not Implemented POST funtionality")


@auth
@audit
# Atiende a funcionalidades por GET definidas por el desarrollador
async def funtionality_GET(segment_1, content=None, **kwargs):
    user = kwargs.get(USER, None)
    request = kwargs.get(REQUEST, None)
    funtionality = kwargs.get(FUNTIONALITY, None)

    request_func = _get_request(request, funtionality, segment_1)

    if hasattr(request_func, RequestKeys.GET):
        if funtionality.type_response == TYPE_RESPONSE_JSON:
            header, result, data = await getattr(request_func, RequestKeys.GET)(
                content=content, user=user
            )

            return JSONResponseAPI(body_header=header, result=result, data=data)

        elif funtionality.type_response == TYPE_RESPONSE_WEB:
            return await getattr(request_func, RequestKeys.GET)(
                user=user, content=content
            )

    else:
        raise HTTPException(status_code=501, detail="Not Implemented GET funtionality")


# Atiende a funcionalidades complejas por POST definidas por el desarrollador
# Buscara la funcionalidad (segment_1), por el metodo POST, y con la subfuncionalidad (segment_2)
@auth
@audit
async def funtionality_complex_POST(segment_1, segment_2, content, **kwargs):
    user = kwargs.get(USER, None)
    request = kwargs.get(REQUEST, None)
    funtionality = kwargs.get(FUNTIONALITY, None)

    header, body = _get_header_body(content)

    request_func = _get_request(request, funtionality, segment_1)

    if hasattr(request_func, RequestKeys.POST):
        if funtionality.type_response == TYPE_RESPONSE_JSON:
            header, result, data = await getattr(request_func, RequestKeys.POST)(
                funtionality=segment_2,
                user=user,
                header=header,
                body=body,
            )

            return JSONResponseAPI(body_header=header, result=result, data=data)

        elif funtionality.type_response == TYPE_RESPONSE_WEB:
            return await getattr(request_func, RequestKeys.POST)(
                user=user, content=content
            )
    else:
        raise HTTPException(status_code=501, detail="Not Implemented POST funtionality")


@auth
@audit
# Atiende a funcionalidades por GET definidas por el desarrollador
async def funtionality_complex_GET(segment_1, segment_2, content=None, **kwargs):
    user = kwargs.get(USER, None)
    request = kwargs.get(REQUEST, None)
    funtionality = kwargs.get(FUNTIONALITY, None)

    request_func = _get_request(request, funtionality, segment_1)

    if hasattr(request_func, RequestKeys.GET):
        if funtionality.type_response == TYPE_RESPONSE_JSON:
            header, result, data = await getattr(request_func, RequestKeys.GET)(
                funtionality=segment_2, user=user, content=content
            )

            return JSONResponseAPI(body_header=header, result=result, data=data)

        elif funtionality.type_response == TYPE_RESPONSE_WEB:
            return await getattr(request_func, RequestKeys.GET)(
                funtionality=segment_2, user=user, content=content
            )
    else:
        raise HTTPException(status_code=501, detail="Not Implemented GET funtionality")


#########################################
################# PROXY #################
#########################################
@auth
@audit
async def proxy_api_GET(segment_1, path, **kwargs):
    response = await ProxyAPI(segment_1, path).get()
    return response


@auth
@audit
async def proxy_api_POST(segment_1, path, content, **kwargs):
    response = await ProxyAPI(segment_1, path).post(content)
    return response


def _get_request(request, funtionality, name):
    if funtionality.type_response == TYPE_RESPONSE_JSON:
        path = Obj.FUNTIONALITY_PATH

    elif funtionality.type_response == TYPE_RESPONSE_WEB:
        path = Obj.WEB_PATH

    return Obj.instance_request(
        name=name,
        params=[funtionality.id, request],
        path=path,
    )


def _get_header_body(content):
    try:
        header = content.get(RequestKeys.HEADER, {})
        body = content.get(RequestKeys.BODY, {})

        if not header and not body:
            body = content

        return header, body

    except Exception as e:
        print("ERROR: Request handler -> get_header_body: " + str(e))

    return None, None


#########################################
################## WEB ##################
#########################################
# @auth
# @audit
# # Atiende a funcionalidades por POST definidas por el desarrollador
# async def funtionality_web_post(segment_1, content, **kwargs):
#     funtionality = kwargs.get(FUNTIONALITY, None)
#     user = kwargs.get(USER, None)

#     request = Obj.instance_request_api(params=[funtionality.id], name=segment_1)
#     if hasattr(request, RequestKeys.POST):
#         html = await getattr(request, RequestKeys.POST)(user, content)

#         return HTMLResponse(html)
#     else:
#         raise HTTPException(status_code=501, detail="Not Implemented POST funtionality")


# @auth
# @audit
# # Atiende a funcionalidades por POST definidas por el desarrollador
# async def funtionality_web_get(segment_1, content, **kwargs):
#     funtionality = kwargs.get(FUNTIONALITY, None)
#     user = kwargs.get(USER, None)

#     request = Obj.instance_request_web(params=[funtionality.id], name=segment_1)
#     if hasattr(request, RequestKeys.GET):
#         html = await getattr(request, RequestKeys.GET)(user, content)

#         return HTMLResponse(html)
#     else:
#         raise HTTPException(status_code=501, detail="Not Implemented GET funtionality")
