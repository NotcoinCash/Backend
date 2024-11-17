from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.database import async_session_factory
from src.users.dependencies import check_auth_header
from src.users.models import User, Boost, Task, users_tasks
from src.users.schemas import UserGetScheme, UserCreateScheme, ReferralsGetScheme, TasksGetScheme, \
    UpdateUserBoostsInfoScheme, UpdateUserTasksScheme

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{user_id}/friends")
async def get_user_friends(user_id: int, user_telegram_id: int = Depends(check_auth_header)):
    # if user_id != user_telegram_id:
    #     return {
    #         "status": "error",
    #         "message": "Telegram id does not match"
    #     }

    async with async_session_factory() as session:
        result = await session.execute(
            select(User)
            .options(joinedload(User.referrals))
            .where(User.id == user_id)
        )

        user = result.scalar()
        if not user:
            return {
                "status": "error",
                "message": "User not found"
            }

        referrals = user.referrals
        return {
            "status": "success",
            "message": "User found, referrals fetched",
            "data": {"user_id": user.id, "referrals": [ReferralsGetScheme.model_validate(referral).model_dump() for referral in referrals]}
        }


@router.get("/{user_id}/tasks")
async def get_user_tasks(user_id: int, user_telegram_id: int = Depends(check_auth_header)):
    # if user_id != user_telegram_id:
    #     return {
    #         "status": "error",
    #         "message": "Telegram id does not match"
    #     }

    async with async_session_factory() as session:
        user = await session.execute(
            select(User).where(User.id == user_id)
        )
        user = user.scalar()
        if not user:
            return {
                "status": "error",
                "message": "User not found"
            }

        completed_tasks = await session.execute(
            select(Task)
            .join(users_tasks)
            .where(users_tasks.c.user_id == user_id)
        )
        completed_tasks = completed_tasks.scalars().all()

        uncompleted_tasks = await session.execute(
            select(Task)
            .outerjoin(users_tasks)
            .where(users_tasks.c.user_id != user_id)
        )
        uncompleted_tasks = uncompleted_tasks.scalars().all()

        return {
            "status": "success",
            "message": "User found, tasks fetched",
            "data": {
                "user_id": user.id,
                "completed_tasks": [
                    TasksGetScheme.model_validate(task).model_dump() for task in completed_tasks
                ],
                "uncompleted_tasks": [
                    TasksGetScheme.model_validate(task).model_dump() for task in uncompleted_tasks
                ]
            }
        }


@router.get("/{user_id}/boosts")
async def get_user_boosts(user_id: int, user_telegram_id: int = Depends(check_auth_header)):
    # if user_id != user_telegram_id:
    #     return {
    #         "status": "error",
    #         "message": "Telegram id does not match"
    #     }

    async with async_session_factory() as session:
        user = await session.execute(
            select(User).where(User.id == user_id)
        )
        user = user.scalar()
        if not user:
            return {
                "status": "error",
                "message": "User not found"
            }

        return {
            "status": "success",
            "message": "User found",
            "data": {"user_id": user.id, "boosts_info": user.boosts_info}
        }


@router.get("/{user_id}")
async def get_user(user_id: int, user_telegram_id: int = Depends(check_auth_header)):
    # if user_id != user_telegram_id:
    #     return {
    #         "status": "error",
    #         "message": "Telegram id does not match"
    #     }
    async with async_session_factory() as session:
        user = await session.execute(
            select(User).where(User.id == user_id)
        )
        user = user.scalar()
        if not user:
            return {
                "status": "error",
                "message": "User not found"
            }

        return {
            "status": "success",
            "message": "User found",
            "data": {"user": UserGetScheme.model_validate(user).model_dump()}
        }


@router.post("/")
async def create_user(new_user_data: UserCreateScheme, user_telegram_id: int = Depends(check_auth_header), referrer_id: Optional[int] = None):
    # if new_user_data.id != user_telegram_id:
    #     return {
    #         "status": "error",
    #         "message": "Telegram id does not match"
    #     }
    async with async_session_factory() as session:
        existing_user = await session.execute(
            select(User).where(User.id == new_user_data.id)
        )
        existing_user = existing_user.scalar()
        if existing_user:
            return {
                "status": "error",
                "message": "User already exists"
            }

        new_user = User(id=new_user_data.id, username=new_user_data.username)

        if referrer_id:
            referrer = await session.execute(
                select(User).where(User.id == referrer_id)
            )
            referrer = referrer.scalar()
            if referrer:
                new_user.referrer = referrer

        boosts = await session.execute(select(Boost))
        default_boosts_info = {}
        for boost in boosts.scalars():
            default_boosts_info[boost.name] = {
                "id": boost.id,
                "level": 1,
                "base_value": boost.base_value,
                "value_per_level": boost.value_per_level,
                "base_upgrade_cost": boost.base_cost,
                "upgrade_cost_per_level": boost.cost_per_level,
                "max_level": boost.max_level
            }

        new_user.boosts_info = default_boosts_info

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        return {
            "status": "success",
            "message": "User successfully created",
            "data": {"user": UserGetScheme.model_validate(new_user).model_dump()}
        }


@router.patch("/update-boosts-info")
async def update_user_boosts_info(update_info: UpdateUserBoostsInfoScheme, user_telegram_id: int = Depends(check_auth_header)):
    # if update_info.user_id != user_telegram_id:
    #     return {
    #         "status": "error",
    #         "message": "Telegram id does not match"
    #     }

    async with async_session_factory() as session:
        user = await session.execute(
            select(User).where(User.id == update_info.user_id)
        )
        user = user.scalar()
        if not user:
            return {
                "status": "error",
                "message": "User not found"
            }

        boost = await session.execute(
            select(Boost).where(Boost.id == update_info.boost_id)
        )
        boost = boost.scalar()
        if not boost:
            return {
                "status": "error",
                "message": f"Boost with id {update_info.boost_id} not found"
            }

        if update_info.boost_level > boost.max_level or update_info.boost_level < 1:
            return {
                "status": "error",
                "message": f"Boost level is incorrect"
            }

        update_cost = boost.base_cost + (boost.cost_per_level * (update_info.boost_level - 1))
        if user.balance < update_cost:
            return {
                "status": "error",
                "message": "Not enough balance"
            }

        user.boosts_info[boost.name]["level"] = update_info.boost_level
        user.balance -= update_cost

        session.add(user)
        await session.commit()
        await session.refresh(user)

        return {
            "status": "success",
            "message": "Boosts info updated",
            "data": {"user_id": user.id, "boost_name": boost.name, "level": update_info.boost_level, "balance": user.balance}
        }


@router.patch("/update-user-tasks")
async def update_user_tasks(update_info: UpdateUserTasksScheme, user_telegram_id: int = Depends(check_auth_header)):
    # if update_info.user_id != user_telegram_id:
    #     return {
    #         "status": "error",
    #         "message": "Telegram id does not match"
    #     }

    async with async_session_factory() as session:
        user = await session.execute(
            select(User).where(User.id == update_info.user_id)
        )
        user = user.scalar()
        if not user:
            return {
                "status": "error",
                "message": "User not found"
            }

        task = await session.execute(
            select(Task).where(Task.id == update_info.task_id)
        )
        task = task.scalar()
        if not task:
            return {
                "status": "error",
                "message": f"Task with id {update_info.task_id} not found"
            }
        user_tasks = await session.execute(
            select(users_tasks).where(users_tasks.c.user_id == user.id)
        )
        user_tasks = user_tasks.scalars().all()

        if task in user_tasks:
            return {
                "status": "error",
                "message": "Task already completed"
            }

        user.tasks.append(task)
        user.balance += task.reward

        session.add(user)
        await session.commit()
        await session.refresh(user)

        return {
            "status": "success",
            "message": "User tasks updated",
            "data": {"user_id": user.id, "tasks_id": task.id, "balance": user.balance, "reward": task.reward}
        }



