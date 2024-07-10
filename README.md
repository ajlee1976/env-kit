# env_kit

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) <br>
Author: [ajlee1976](https://github.com/ajlee1976)

EnvKit is a way to have typed environment variables within Python. Default OS Environment arguments *cannot* be defined into a type,
and instead they must be a string, and thus EnvKit defines the typed version into a `Config` class. These variables are also
put into the environment via the typical `os` module, however these types are stringified. 

### Configuration & General Use
You define an environment variable by the following format: <br>
`KEY=TYPE=VALUE`

You can also use comments in the file by using a `#` character.
``` 
# A full line comment works
EXAMPLE=INT=1  # Or an inline comment also will work
```

#### Initialising an environment
```py
env_kit.Config.from_file("./Path/To/Your/File")
```

#### Querying environment variables
As mentioned above, variables passed into EnvKit are defined into both the Config class, as well as the `os` environment
variables. You can access the typed variables via:
```py
cfg = env_kit.Config.from_file("./Path/To/Your/File")
cfg.YOUR_VARIABLE
```
or you can access the stringified OS environment variables by:
```py 
import os
os.getenv("YOUR_VARIABLE")
```

If you wish, you can also configure a custom `Config` class where you create type hinted definitions, or any utility functions.
```py 
import env_kit
class CustomConfig(env_kit.Config):
    MY_VARIABLE: str
    MY_BOOLEAN: bool

cfg = CustomConfig.from_file("./Path/To/Your/File")
cfg.MY_VARIABLE
```
### Current Supported Types
| EnvKit Type | Common Type | Python Type |
|:-----------:|:-----------:|:-----------:|
|     STR     |   String    |     str     |
|     INT     |   Integer   |     int     |
|    BOOL     |   Boolean   |    bool     |
|    JSON     |    JSON     |    dict     |
|     ARR     |    Array    |    list     |


If no value is passed, then the kit will default to use `None`. <br>
**\* Note that if no type is passed (see the below example), it is defaulted to be a string.**

### Example Environment File
```
INT_TEST=INT=123
STR_TEST=STR=Hello World
BOOL_TEST=BOOL=FALSE
JSON_TEST=JSON={"hello": "World", "inner": {"inner_key": "inner_value"}}
ARR_TEST=ARR=["Element 1", "Element 2", 3, "Element 4"]
RAW_STR=Hello World Part 2
RAW_STR_AGAIN=123
# This will be set to `None`
NULL_TEST=INT=
```
