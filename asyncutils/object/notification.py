# -*- coding : utf-8 -*-

import asyncio
from asyncutils import MessageCondition


class Notification:

    """
    A Notification instance, NOT thread-safe

    A Notification is a synchronization object which allows passing
    notification messages between waiting coroutines. This also ensures
    that once a notification is sent all the waiting coroutines must wake
    up and get the message before a another notification can be sent.

    :param asyncio.Lock lock: Lock to be used for shared access.
                              If None (default) then new lock will be used.

    The intended way of using this coroutine is shown below;

    Sending notifications

    >>> notification = Notification()
    >>> await notification.send(msg="hello world!")

    Receiving notifications

    >>> msg = await notification.recv()
    >>> print(msg)
    hello world!

    """

    def __init__(self, lock=None):

        self._notify_condition = MessageCondition(lock=lock)
        self.__wake_up_done_event = asyncio.Event()
        self.__wake_up_done_event.set()

        self.__wake_n = 0

    async def send(self, *, n=-1, msg=None):
        """
        Coroutine for sending notifications to waiting coroutines.
        If there are no waiting coroutines then this will result in a NO-OP

        :param int n: keyword-only argument specifying number of coroutines to
                      send. if -1 (default) then all coroutines will be
                      awakened.
        :param Any msg: msg to be sent to the waiting coroutines
                        (default is None)

        """
        await self.__wake_up_done_event.wait()

        if n_waiters:= len(self._notify_condition._waiters):
            self.__wake_n = n_waiters if n < 0 else n

        if self.__wake_n > 0:
            self.__wake_up_done_event.clear()

        async with self._notify_condition:
            self._notify_condition.notify(n=self.__wake_n, msg=msg)

    async def recv(self):
        """
        Coroutine for receiving notifications
        """
        async with self._notify_condition:
            msg = await self._notify_condition.wait()
            self.__wake_n -= 1

        if self.__wake_n == 0:
            self.__wake_up_done_event.set()

        return msg
