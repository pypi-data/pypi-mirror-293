from __future__ import annotations

from collections.abc import Awaitable, Callable

from ... import client
from ...punish import Punish
from ...typing import Thread
from ..user_checker import _user_checker

TypeThreadChecker = Callable[[Thread], Awaitable[Punish | None]]


def __id_checker(func):
    """
    装饰器: 使用历史状态缓存避免重复检查
    """

    async def _(thread: Thread) -> Punish | None:
        prev_last_time = client._db_sqlite.get_id(thread.tid)
        if prev_last_time is not None:
            if thread.last_time == prev_last_time:
                return
            if thread.last_time < prev_last_time:
                client._db_sqlite.add_id(thread.tid, tag=thread.last_time)
                return

        punish = await func(thread)
        if punish:
            return punish

        client._db_sqlite.add_id(thread.tid, tag=thread.last_time)

    return _


async def __default_checker(_):
    pass


ori_checker: TypeThreadChecker = __default_checker
checker: TypeThreadChecker = _user_checker(ori_checker)


_set_checker_hook = None


def set_checker(
    enable_user_checker: bool = True,
    enable_id_checker: bool = True,
) -> Callable[[TypeThreadChecker], TypeThreadChecker]:
    """
    装饰器: 设置主题帖检查函数

    Args:
        enable_user_checker (bool, optional): 是否检查发帖用户的黑白名单状态. Defaults to True.
        enable_id_checker (bool, optional): 是否使用历史状态缓存避免重复检查. Defaults to True.

    Returns:
        Callable[[TypeThreadChecker], TypeThreadChecker]
    """

    def _(new_checker: TypeThreadChecker) -> TypeThreadChecker:
        if new_checker is __default_checker:
            return new_checker

        _set_checker_hook()

        global ori_checker, checker
        ori_checker = new_checker
        checker = ori_checker

        if enable_user_checker:
            checker = _user_checker(checker)
        if enable_id_checker:
            checker = __id_checker(checker)

        return ori_checker

    return _
