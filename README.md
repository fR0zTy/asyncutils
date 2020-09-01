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

A LoggedLock is an extension of asyncio.Lock which logs its state when
acquired and released. In addition to its state, it also allows to pass
additional messages which are logged during acquisition and release of
the lock.


`:param Optional[str] name: An optional name for the lock used during logging`

`:param logging.Logger logger: Logger instance used for logging (default is root)`

`:param int level: logging level for the log messages (default is 10, which is logging.DEBUG)`


The intended way of using this is similar to asyncio.Lock
```
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

