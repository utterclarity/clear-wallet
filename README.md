clear-wallet
============

An online wallet designed for simple interaction with BlooCoin.

Requirements
------------

+ `flask`
+ `wtforms`
+ `flask-wtf` (for improved form security, yo)

configuration
-------------

First off, rename `config.json.sample` to `config.json`. This file contains information for Flask's app settings. Namely the `SECRET_KEY`.

The contents should look something like this:
```javascript
{
    "SECRET_KEY": "__secret__"
}
```

Get a good secret key via `os.urandom(24)` in Python, then C/P the results above.

TODO
----

+ Add uploading of wallet file to log in.
+ Generate new wallet file and log in. __Done!__
+ Download wallet file. __Done!__
