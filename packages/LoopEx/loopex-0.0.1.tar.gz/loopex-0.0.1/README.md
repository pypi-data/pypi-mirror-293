# LoopEx

A extension enhancing Python loop.

## Usage

First, install package via pip.

```
pip install loopex@git+https://github.com/glyzinieh/python-loop-extension
```

Second, import module before the loop.

```Python
from loopex import LoopEx
```

## Features

Now, one feature is available. We plan to add more features in the future.

### `do_while(condition)`

This enables you to implement "do...while" in Python in a simple way. This is similar to the while statement, but the expression is tested after the suite is executed.

```Python
do_while = LoopEx().do_while
result = ''
i = 0

while do_while(i < 5):
    i += 1
    result += str(i)

print(result) # 12345
```
