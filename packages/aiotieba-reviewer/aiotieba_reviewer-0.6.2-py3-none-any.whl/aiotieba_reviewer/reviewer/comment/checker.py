from __future__ import annotations

from collections.abc import Awaitable, Callable

from ... import client
from ...punish import Punish
from ...typing import Comment
from ..user_checker import _user_checker

TypeCommentChecker = Callable[[Comment], Awaitable[Punish | None]]


def __id_checker(func):
    """
    装饰器: 使用历史状态缓存避免重复检查
    """

    async def _(comment: Comment) -> Punish | None:
        if client._db_sqlite.get_id(comment.pid) is not None:
            return

        punish = await func(comment)
        if punish:
            return punish

        client._db_sqlite.add_id(comment.pid)

    return _


async def __default_checker(_):
    pass


ori_checker: TypeCommentChecker = __default_checker
checker: TypeCommentChecker = _user_checker(ori_checker)


_set_checker_hook = None


def set_checker(
    enable_user_checker: bool = True,
    enable_id_checker: bool = True,
) -> Callable[[TypeCommentChecker], TypeCommentChecker]:
    """
    装饰器: 设置楼中楼检查函数

    Args:
        enable_user_checker (bool, optional): 是否检查发帖用户的黑白名单状态. Defaults to True.
        enable_id_checker (bool, optional): 是否使用历史状态缓存避免重复检查. Defaults to True.

    Returns:
        Callable[[TypeCommentChecker], TypeCommentChecker]
    """

    def _(new_checker: TypeCommentChecker) -> TypeCommentChecker:
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
