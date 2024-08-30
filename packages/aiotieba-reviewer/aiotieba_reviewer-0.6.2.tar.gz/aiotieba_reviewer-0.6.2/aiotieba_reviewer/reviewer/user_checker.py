from __future__ import annotations

from ..client import get_db
from ..enums import Ops
from ..punish import Punish
from ..typing import TypeObj


def _user_checker(func):
    """
    装饰器: 检查发帖用户的黑白名单状态

    发现黑名单用户则删帖并封十天
    """

    async def _(obj: TypeObj) -> Punish | None:
        db = await get_db()
        permission = await db.get_user_id(obj.user.user_id)
        if permission <= -50:
            return Punish(obj, Ops.DELETE, 10, "黑名单")
        if permission >= 10:
            return Punish(obj, Ops.NORMAL)
        return await func(obj)

    return _
