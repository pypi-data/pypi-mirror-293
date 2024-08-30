from app.service.request.request import Request
from fastapi.templating import Jinja2Templates


class RequestView(Request):

    def __init_subclass__(self):
        self.templates = Jinja2Templates(directory="app/resource/view")
        # return super().__init_subclass__()

    def render(self, template_name: str, context: dict = {}):
        context["request"] = self.request

        template_name += ".html"
        return self.templates.TemplateResponse(template_name, context)
