# Description
This library provides the ability of converting django logs to JSON.

# Requirements
- Python 3.11 or higher
- Django 3.2 or higher

# Installation
Using standard Json library:
```shell
pip install django-json-logger
```

### Custom json libraries

#### Orjson
To use [Orjson](https://github.com/ijl/orjson):
```shell
pip install django-json-logger[orjson]
```
and add to Django settings `LOGGING_SERIALIZER="orjson"`

#### Ujson
To use [Ujson](https://github.com/ultrajson/ultrajson):
```shell
pip install django-json-logger[ujson]
```
and add to Django settings `LOGGING_SERIALIZER="ujson"`

**Note**:  If you're using zsh you need to escape square brackets: pip install ... \[ujson\]

# Development

## Testing
The package is tested against multiple Python and Django versions using nox:

- Python versions: 3.11, 3.12
- Django versions: 3.2, 4.2, 5.1

To run the tests:

```shell
# Install development dependencies
pip install -e ".[dev]"

# Run tests with nox
nox

# Run tests for specific environment
nox -s "tests-3.11(django='django>=4.2,<4.3')"
```

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
