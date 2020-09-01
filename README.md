# asyncutils
## General-purpose asynchronous utillities for Python

This package contains a collection of objects which are built using python's standard library, and designed to be compatible with python's [asyncio](https://docs.python.org/3/library/asyncio.html) package.

## Installation Notes:

**The minimum required version for python is 3.8**

1. Clone the repo to your filesystem from [here](https://github.com/fR0zTy/asyncutils)
2. Then change your current directory to the cloned repository (directory containing `setup.py` file)
```
>cd <path_to_package>
```

3. Make sure you are using the appropriate python version, and run the following command from terminal

```
>python -m pip install .
```

## Contents

### 1. LoggedLock

`LoggedLock(name=None, logger=logging, level=logging.DEBUG)`

LoggedLock instance, NOT thread-safe

A LoggedLock is an extension of [`asyncio.Lock`](https://docs.python.org/3/library/asyncio-sync.html#asyncio.Lock) which logs its state when
acquired and released. In addition to its state, it also allows to pass
additional messages which are logged during acquisition and release of
the lock.


`:param Optional[str] name: An optional name for the lock used during logging`

`:param logging.Logger logger: Logger instance used for logging (default is root)`

`:param int level: logging level for the log messages (default is 10, which is logging.DEBUG)`


The intended way of using this is similar to [`asyncio.Lock`](https://docs.python.org/3/library/asyncio-sync.html#asyncio.Lock)
```
>>> from asyncutils import LoggedLock
>>> lock = LoggedLock(name="hello_world_lock", level=logging.INFO)
>>> async with lock:
>>>     await asyncio.sleep(0.1)
root - INFO - hello_world_lock waiting for acquisition.
root - INFO - hello_world_lock acquired.
root - INFO - hello_world_lock released.
```

Logging additional information from separate tasks

```
>>> async with lock("In foobar task"):
>>>     await asyncio.sleep(0.1)
root - INFO - hello_world_lock waiting for acquisition. In foobar task
root - INFO - hello_world_lock acquired. In foobar task
root - INFO - hello_world_lock released. In foobar task
```

### 2. MessageCondition

`MessageCondition(lock=None)`

A MessageCondition instance, NOT thread-safe

A MessageCondition is an extension of [`asyncio.Condition`](https://docs.python.org/3/library/asyncio-sync.html#asyncio.Condition) that allows passing messages to the waiting coroutines.

`:param asyncio.Lock lock: An optional lock instance to be used by condition. If None then a new lock will be used`

The intended way to use the instances of this class is same as using
[`asyncio.Condition`](https://docs.python.org/3/library/asyncio-sync.html#asyncio.Condition)

Sending messages to all waiters

```
>>> from asyncutils import MessageCondition
>>> msg_cond = MessageCondition()
>>> async with msg_cond:
>>>     msg_cond.notify_all(msg="hello world!")
```

Sending messages to `n` waiters
```
>>> async with msg_cond:
>>>     msg_cond.notify(n=2, msg="hello world!")
```

Waiting for notifications

```
>>> async with msg_cond:
>>>     msg = await msg_cond.wait()
>>> print(msg)
hello world!
```