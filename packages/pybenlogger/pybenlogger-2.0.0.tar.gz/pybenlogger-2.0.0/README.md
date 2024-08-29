# pybenlogger
Unified logger format

## Use options:

1. Direct import from base module
```python
from pybenlogger import get_logger

logger = get_logger()
```
2. Import from the inner module
```python
from pybenlogger.config_logger import get_logger

logger = get_logger(logger_name='main_logger')
```

## get_logger:
Returns a logger object with a given title, default name as 'main_logger'

:param logger_name: If empty the logger name will be based on the calling module

:return: Logger object