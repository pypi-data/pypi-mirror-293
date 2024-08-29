# Contextual Logger

## Usage

``` python
import logging
import contextual_logger

logger = logging.getLogger("name")

def process_example(ex):
  logger.info("Processing example by doing ...")
  return ex

data = ...

with logger(dataset="SST2"):
  data = [process_example(d) for d in data]
```

``` json
{
  "level_name": "INFO",
  "timestamp": "...",
  "logger": "demo",
  "message": "Processing example by doing ...",
  "dataset": "SST2"
}
{
  "level_name": "INFO",
  "timestamp": "...",
  "logger": "demo",
  "message": "Processing example by doing ...",
  "dataset": "SST2"
}
```
