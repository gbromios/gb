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

gb.daemon
---------

have you ever wanted to run something as a daemon, but only wanted to write a
single method to deal with it? just define a method:

```
def daemon_business(self, importance):
	if importance:
		print("doing important stuff")
		# ...

	else:
		print("just chillin")
```

that method is called when the daemon starts, then once that method returns, the 
server cleans up.

```
my_d = gb.daemon.Daemon(name="importantd")
my_d.start(daemon_business, start_params = { "importance": 9000 })
```

the forking and so forth happens here in start. you should make any method that
manages this stuff respond to the return codes from Daemon.start() (e.g., the
script you are using to configure and start a daemon)

0 - process that was started initially. this is generally where you want any
  init script to print `[ OK ]` or `[FAIL]` type messages; other exit codes should
  trigger instance termination of the script.

1 - intermediate process, child of the first fork, parent of the second fork.
  you generally just want to exit after getting this one.

2 - this is the second child process, the actual daemon that will be running in
  the bg. This is the only process that will ever hit your passed in start_fn,
  the previous two "forks" will exit Daemon.start() before getting that far.

still a bit rough around the edges. when I get some time, I'd like to integrate
the management side (start/stop/etc) to make it a bit more self-contained and
simple to start using immediately.
