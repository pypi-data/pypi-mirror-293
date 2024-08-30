from fastapi.encoders import jsonable_encoder

from app.service.response.header import HeaderAPI, HeaderKeys
from app.service.response.result import ResultAPI


class JSONResponseAPI:

    def __init__(
        self,
        body_header=None,
        result=None,
        data=None,
    ):
        if body_header:
            if isinstance(body_header, HeaderAPI):
                self.header = body_header
            elif isinstance(body_header, dict):
                channel = body_header.get(HeaderKeys.CHANNEL, None)
                language = body_header.get(HeaderKeys.LANGUAGE, None)
                version = body_header.get(HeaderKeys.VERSION, None)
                self.header = HeaderAPI(
                    channel=channel, language=language, version=version)
            else:
                self.header = HeaderAPI()

        if result:
            self.result = result
        else:
            self.result = ResultAPI()

        if data is not None:
            self.body = data

    # def __call__(self):
    #     # return JSONResponse(
    #     #     # status_code=self.status_code,
    #     #     # content=self.content,
    #     #     # headers=self.headers,
    #     #     # media_type=self.media_type,
    #     #     # background=self.background,
    #     # )
    #     pass


# class FormatResponseMiddleware(BaseHTTPMiddleware):

#     def __init__(self, app: ASGIApp, header_value: str):
#         super().__init__(app)
#         self.header_value = header_value

#     # def __init__(self, app: ASGIApp) -> None:
#     #         self.app = app

#     # async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
#     #     scope["path"] = scope["path"].replace("foo", "bar")
#     #     await self.app(scope, receive, send)

#     async def dispatch(self, request, call_next):
#         print("Entro middleware")
#         response = await call_next(request)

#         if hasattr(response, "body_iterator"):
#             res_body = b""
#             async for chunk in response.body_iterator:
#                 res_body += chunk

#             body = St.decode(res_body)

#             formatted_response = {
#                 ResponseKeys.REQUEST_KEY: request.url.path,
#                 ResponseKeys.STATUS_KEY: response.status_code,
#                 ResponseKeys.DATA_KEY: body,
#             }

#             response_json = json.dumps(formatted_response)
#             print(response_json)
#             return Response(
#                 content=response_json,
#                 status_code=response.status_code,
#                 media_type="application/json",
#             )
