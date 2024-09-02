from collections.abc import Awaitable, Callable

from ...client import get_client
from ...typing import Comment, Post

TypeCommentsProducer = Callable[[Post], Awaitable[list[Comment]]]


async def __default_producer(post: Post) -> list[Comment]:
    client = await get_client()

    reply_num = post.reply_num
    if reply_num > 10 or (len(post.comments) != reply_num and reply_num <= 10):
        last_comments = await client.get_comments(post.tid, post.pid, pn=post.reply_num // 30 + 1)
        comment_set = set(post.comments)
        comment_set.update(last_comments.objs)
        comment_list = list(comment_set)

    else:
        comment_list = post.comments

    return comment_list


producer: TypeCommentsProducer = __default_producer


def set_producer(new_producer: TypeCommentsProducer) -> TypeCommentsProducer:
    global producer
    producer = new_producer
    return new_producer
