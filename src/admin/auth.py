from typing import Union

from sqladmin.authentication import AuthenticationBackend
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse

from src.config import settings


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        if username != settings.ADMIN_USERNAME or password != settings.ADMIN_PASSWORD:
            return False

        request.session.update({"token": settings.ADMIN_AUTH_TOKEN})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Union[bool, RedirectResponse]:
        token = request.session.get("token")

        if not token:
            return RedirectResponse(url=request.url_for("admin:login"), status_code=status.HTTP_302_FOUND)

        return token == settings.ADMIN_AUTH_TOKEN
