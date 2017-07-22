znc-log-browser
=======

This is a module for [ZNC](http://znc.in) which provides web-based log browsing capability for the built-in [log](https://wiki.znc.in/Log) module.

## Installation

### Required Modules

You must have these modules installed in order to use this one.

* ```modpython``` - should be installed, this is a Python 3 module.
* ```log``` - currently, this must be installed as a **user** module.
* ```webadmin``` - this plugin exposes itself via the webadmin interface

### Copying the files

Copy ```logbrowser/``` and ```logbrowser.py``` to your modules directory. Typically, this is in ```~/.znc/modules```:

```
cp -R logbrowser/ logbrowser.py ~/.znc/modules
```

### Enable it in ZNC

You can enable this module either via the webadmin interface or with the following IRC command:

```
/quote znc LoadModule logbrowser
```

Enjoy!