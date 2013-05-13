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

You have to make a file called `config.json` in the directory of `main.py`, which
contains information for Flask's app settings. Namely the `SECRET_KEY`.

Make the contents something like this:
```javascript
{
    "SECRET_KEY": "__secret__"
}
```

Get a good secret key via `os.urandom(24)` in Python, then C/P the results above.
