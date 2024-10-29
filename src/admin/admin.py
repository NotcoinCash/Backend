from sqladmin import Admin, ModelView

from src.admin.auth import AdminAuth
from src.config import settings
from src.database import async_engine
from src.users.models import User, Boost, Task

authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)


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
