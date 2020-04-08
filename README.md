# dirwatcher-demo

Directory monitoring application written in Python

This utility will recursively monitor a given directory for the presence
of files ending in a specified extension for the presence of a given
text string. It is assumed that monitored files will only ever be
added, removed, or appended to (not edited),
as in the case of typical log files.

usage: dirwatcher.py [-h][-e ext] [-i INTERVAL] path magic

positional arguments:
path Directory path to watch
magic String to watch for

optional arguments:
-h, --help show help message and exit
-e EXT, --ext EXT Text file extension to watch
-i INTERVAL, --interval INTERVAL
Number of seconds between polling

This application was developed with Python 3.7.7.
PIP modules used in development include:
astroid==2.3.3
autopep8==1.5
entrypoints==0.3
flake8==3.7.9
isort==4.3.21
lazy-object-proxy==1.4.3
mccabe==0.6.1
pycodestyle==2.5.0
pyflakes==2.1.1
pylint==2.4.4
six==1.14.0
typed-ast==1.4.1
wrapt==1.11.2

These may be installed via script with the included requirements.txt file.
