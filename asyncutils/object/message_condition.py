# -*- coding : utf-8 -*-

import asyncio


class MessageCondition(asyncio.Condition):
    """
    A MessageCondition instance, NOT thread-safe

    A MessageCondition is an extension of asyncio.Condition that allows
    passing messages to the waiting coroutines.

    The intended way to use the instances of this class is same as using
    asyncio.Condition

    Sending notifications

    >>> msg_cond = MessageCondition()
    >>> async with msg_cond:
    >>>     msg_cond.notify_all(msg="hello world!")

    Waiting for notifications

    >>> async with msg_cond:
    >>>     msg = await msg_cond.wait()
    >>> print(msg)
    hello world!

    """

    def __init__(self, lock=None):
        super().__init__(lock=lock)
        self._msg = None

    def notify(self, n=1, *, msg=None):
        """
        wake up at most n tasks waiting on the condition with given message.
        default is 1
        :param int n: Number of tasks to wake
        :param Any msg: keyword-only argument containing message
        :raises: RuntimeError if called without acquiring the underlying lock
        """
        self._msg = msg
        super().notify(n=n)

    def notify_all(self, *, msg=None):
        """
        wake up all tasks waiting on the condition
        :param Any msg: keyword-only argument containing message
        :raises: RuntimeError if called without acquiring the underlying lock
        """
        self.notify(n=len(self._waiters), msg=msg)

    async def wait(self):
        """
        coroutine for waiting on condition
        :raises: RuntimeError if called without acquiring the underlying lock
        """
        await super().wait()
        return self._msg
