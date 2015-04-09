gb
====================

assorted utility libs

gb (n) an arbitrary two letter namespace

gb.http
-------

Lightweight http server, good for quick protypes/small projects

 - check http/test.py to see a small illustration of adding routes and running
   a server

 - see https://docs.python.org/2/library/basehttpserver.html to look at
   useful BaseHTTPRequestHandler fields/methods

gb.options
----------

options files. like this:

```
some_setting = "500 degrees"
another_thing = bills_house
authorized_users = [ rusty_s, p_willeaux, tony_p ]
sports = {
	base = ball,
	tenn = is
}

```
they are options objects which basically turn into dicts, and can be attached to
Optionable subclasses or made global or passed around in whichever manner you prefer.

the whitespace is simple, so you can get a tiny bit fancier with layout
but it's not really meant for anything beyond simple config files
