# pylogserver Python Package

As a companion executable to `logging.handlers.SocketHandler`.

## Example

Start server from cmdline:

```plain
$ pip install pylogserver
$ pylogserver 9999
Listening on localhost:9999
```

Client side example:

```python
#!/usr/bin/env python3
# client.py
import logging
import logging.handlers

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    socket_handler = logging.handlers.SocketHandler('localhost', 9999)
    logger.addHandler(socket_handler)
    logger.info('Hello, world!')
```

Server side output:

```plain
[2024-08-28 20:26:04,681] [root] [INFO] Hello, world!
```

## References

- [Python official logging cookbook](https://docs.python.org/zh-cn/3/howto/logging-cookbook.html#sending-and-receiving-logging-events-across-a-network)
