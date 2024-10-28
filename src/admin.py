from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from src.database import async_engine
from src.users.models import User, Boost, Task


class AdminAuth(AuthenticationBackend):
    # async def login(self, request: Request) -> bool:
    #     form = await request.form()
    #     username, password = form["username"], form["password"]
    #     return True

    # async def logout(self, request: Request) -> bool:
    #     return True

    async def authenticate(self, request: Request) -> bool:
        return True


authentication_backend = AdminAuth(secret_key="")


def init_admin(app):
    admin = Admin(
        app=app,
        engine=async_engine,
        authentication_backend=authentication_backend
    )

    class UserAdmin(ModelView, model=User):
        column_list = [User.id, User.joined_at, User.is_active]

    class TaskAdmin(ModelView, model=Task):
        column_list = [Task.id, Task.name]

    class BoostAdmin(ModelView, model=Boost):
        column_list = [Boost.id, Boost.name]

    admin.add_view(UserAdmin)
    admin.add_view(TaskAdmin)
    admin.add_view(BoostAdmin)