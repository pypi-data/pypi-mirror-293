import datetime
import logging

from fastapi import APIRouter
from pydantic_db_backend.backend import Backend

from eventix.functions.task import task_post, task_by_unique_key, task_reschedule
from eventix.pydantic.task import TaskModel

log = logging.getLogger(__name__)

router = APIRouter(tags=["task"])


@router.post("/task")
async def route_task_post(task: TaskModel) -> TaskModel:
    return task_post(task)


@router.get("/task/{uid}")
async def route_task_get(uid: str) -> TaskModel:
    # noinspection PyTypeChecker
    return Backend.client().get_instance(TaskModel, uid)


@router.delete("/task/{uid}")
async def route_task_delete(uid: str) -> None:
    return Backend.client().delete_uid(TaskModel, uid)


@router.get("/task/{uid}/reschedule")
async def route_task_reschedule_get(uid: str, eta: datetime.datetime | None = None):
    return task_reschedule(uid, eta)


@router.get("/task/by_unique_key/{unique_key}")
async def route_task_(unique_key: str) -> TaskModel:
    return task_by_unique_key(unique_key=unique_key)


@router.delete("/task/by_unique_key/{unique_key}")
async def route_task_(unique_key: str) -> None:
    uid = task_by_unique_key(unique_key=unique_key).uid
    return Backend.client().delete_uid(TaskModel, uid)


@router.put("/task/{uid}")
async def route_task_put(uid: str, task: TaskModel) -> TaskModel:
    task.uid = uid  # overwrite uid
    # noinspection PyTypeChecker
    return Backend.client().put_instance(task)
