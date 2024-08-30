
# JIBIX

[![GitHub](https://img.shields.io/github/license/navendu-pottekkat/awesome-readme)](https://img.shields.io/github/license/navendu-pottekkat/awesome-readme)

Jibix is a easy-to-handle database-manager and it's very simple to work with:
```python
from jibix import Jibix
db = Jibix('database name.json')
db['hello'] = 1 # automatically saves in database for next time you loading it
db.pop('hello') # automatically commits in database for next time you loading it
```
Yeah that's it ;)

### don't use jibix when you have more than 20 commits per second


