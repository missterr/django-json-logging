# Description
This library provides the ability of converting django logs to JSON.

# Installation


# Usage
### Django setup

```python
# setting.py

LOGGING_APP_NAME = 'your_app_name'  # required
LOGGING_FIELDS = ('levelname', 'name', 'module', 'process', 'thread', 'pathname', 'asctime')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            '()': 'django_json_logging.formatters.JSONFormatter',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'json',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'WARNING',
        },
        'django': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}

```
Somewhere in the code
```python
import logging

your_json_logger = logging.getLogger('json_logger')
your_json_logger.warning('Something happened here', extra={'event_code': 'xxx'})
```
[Exhaustive fields list can be found here][1]

[1]: https://docs.python.org/3/library/logging.html#logrecord-attributes