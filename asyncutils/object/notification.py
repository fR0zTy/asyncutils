# -*- coding : utf-8 -*-

import asyncio
from asyncutils import MessageCondition


class Notification:

    """
    A Notification instance, NOT thread-safe

    A Notification is a synchronization object which allows passing notification messages between waiting coroutines.
    This also ensures that once a notification is sent all the waiting coroutines must wake up and get the message
    before a another notification can be sent.

    :param asyncio.Lock lock: Lock to be used for shared access. If None (default) then new lock will be used.

    The intended way of using this coroutine is shown below;

    Sending notifications

    >>> notification = Notification()
    >>> await notification.send(msg="hello!")

    Receiving notifications

    >>> msg = await notification.recv()
    >>> print(msg)
    hello!

    Receiving notifications with callbacks

    >>> greet = lambda msg, name: msg + f" {name}."
    >>> msg = await notification.recv(callback=greet, "Frank")
    >>> print(msg)
    hello! Frank.
    """

    def __init__(self, lock=None):

        # Intentionally omitted the loop parameter for future compatibility with python 3.10

        self._notify_condition = MessageCondition(lock=lock)
        self.__wake_up_done_event = asyncio.Event()
        self.__wake_up_done_event.set()

        self.__wake_n = 0

    async def wait_for_all_notified(self):
        """
        Coroutine for waiting for all waiters to get notified

        .. note:: This will return immediately if there are no waiters for the notification
        """
        if not self.__wake_up_done_event.is_set():
            await self.__wake_up_done_event.wait()

    async def send(self, *, n=-1, msg=None):
        """
        Coroutine for sending notifications to waiting coroutines. If there are no waiting coroutines then this
        will result in a NO-OP

        :param int n: keyword-only argument specifying number of coroutines to send. if -1 (default) then all
                      coroutines will be awakened.
        :param Any msg: msg to be sent to the waiting coroutines (default is None)

        """
        n_waiters = len(self._notify_condition._waiters)
        if n_waiters:
            self.__wake_n = n_waiters if n < 0 else n

        if self.__wake_n > 0:
            self.__wake_up_done_event.clear()

        async with self._notify_condition:
            self._notify_condition.notify(n=self.__wake_n, msg=msg)

        await self.wait_for_all_notified()

    async def recv(self, *args, callback=None, **kwargs):
        """
        Coroutine for receiving notifications

        :param Optional[callable] callback: callable which will be executed when a notification is received with msg
                                            as argument. If callback is provided then the result of the callback
                                            will be returned otherwise the the message will be returned.

        .. note:: args and kwargs will be passed into the callback if provided along with the nofitication message
        .. warning:: The callable will be executed with exclusive access. Therefore, other waiters cannot wake up
                     until the callable is done executing. User caution is advised.
        """
        async with self._notify_condition:
            msg = await self._notify_condition.wait()

            if callback is not None:
                if asyncio.iscoroutine(callback):
                    raise TypeError("callback cannot be a coroutine function must be a coroutine or sync function")
                elif asyncio.iscoroutinefunction(callback):
                    ret = await callback(msg, *args, **kwargs)
                elif callable(callback):
                    ret = callback(msg, *args, **kwargs)
                else:
                    raise TypeError(f"Invalid type {type(callback)} for arg callback")
            else:
                ret = msg

            self.__wake_n -= 1

        if self.__wake_n == 0:
            self.__wake_up_done_event.set()

        return ret

    @property
    def _waiters(self):
        return self._notify_condition._waiters
