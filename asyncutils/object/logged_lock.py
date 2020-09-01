# -*- coding : utf-8 -*-

import asyncio
import logging


class LoggedLock(asyncio.Lock):

    def __init__(self, name=None, logger=logging, level=logging.DEBUG):
        """
        LoggedLock instance, NOT thread-safe

        A LoggedLock is an extension of asyncio.Lock which logs its state when acquired and released.
        In addition to its state, it also allows to pass additional messages which are logged during
        acquisition and release of the lock.

        :param Optional[str] name: An optional name for the lock used during logging
        :param logging.Logger logger: Logger instance used for logging (default is root)
        :param int level: logging level for the log messages (default is 10, which is logging.DEBUG)

        The intended way of using this is similar to asyncio.Lock

        >>> lock = LoggedLock(name="hello_world_lock", level=logging.INFO)
        >>> async with lock:
        >>>     await asyncio.sleep(0.1)
        root - INFO - hello_world_lock waiting for acquisition.
        root - INFO - hello_world_lock acquired.
        root - INFO - hello_world_lock released.

        Logging additional information from separate tasks

        >>> async with lock("In foobar task"):
        >>>     await asyncio.sleep(0.1)
        root - INFO - hello_world_lock waiting for acquisition. In foobar task
        root - INFO - hello_world_lock acquired. In foobar task
        root - INFO - hello_world_lock released. In foobar task


        """
        self.name = name or self.__class__.__name__
        self.logger = logger
        self.level = level

        self.__task_info_lut = {}
        super().__init__()

    async def acquire(self):
        info = self.__task_info_lut.get(asyncio.current_task(), "")
        self.logger.log(self.level, f"{self.name} waiting for acquisition. {info}")
        await super().acquire()
        self.logger.log(self.level, f"{self.name} acquired. {info}")

    def release(self):
        info = self.__task_info_lut.get(asyncio.current_task(), "")
        super().release()
        self.logger.log(self.level, f"{self.name} released. {info}")

    def __call__(self, info):
        self.__task_info_lut[asyncio.current_task()] = info
        return self
