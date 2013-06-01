clear-wallet
============

An online wallet designed for simple interaction with BlooCoin.

Running
-------
Wallet is best run via gunicorn:  
`gunicorn -w 3 -k gevent -b :3124 -p ~/gunicorn-wallet.pid main:app`  
It might be more beneficial to bind to a unix socket (`-b unix:/tmp/gunicorn.sock`), allowing somewhat better pass-through with nginx (explained later).

Requirements
------------
You can see the dependencies in the `requirements.txt` file. Install with `pip install -r requirements.txt`  
You might need the `libevent-dev` module to compile gevent successfully.

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

TODO
----

+ Add uploading of wallet file to log in.
+ Generate new wallet file and log in. __Done!__
+ Download wallet file. __Done!__