import sys, os, errno, time, traceback, signal

class DaemonError(Exception):
	pass

class Daemon(object):
	"""simplest daemon i could figure out. I'll add some better docs"""
	def __init__(self, name, pid_dir='/tmp'):
		self.name = name.replace('/','')
		self.pid_path = os.path.join(pid_dir, "%s.pid" % self.name)

	@property
	def pid_is_set(self):
		return os.path.isfile(self.pid_path)

	def set_pid(self):
		with open(self.pid_path, 'w') as pid_file:
			pid_file.write(str(os.getpid()))

	def unset_pid(self):
		os.remove(self.pid_path)

	def stop(self):
		if not self.pid_is_set:
			raise DaemonError(
				"pid not set in %s, is process running?" % self.pid_path
			)

		pid = int(open(self.pid_path, 'r').read().strip())
		os.kill(pid, signal.SIGTERM)
		self.unset_pid()

	def start(self, raw_output_log, start_fn, start_params={}):
		if self.pid_is_set:
			pid = open(self.pid_path).read().strip()
			raise DaemonError(
				"pid %s found in %s\n%s already running or did not exit cleanly"
				% (pid, self.pid_path, self.name)
			)

		# become a daemon
		pid = os.fork()
		# parent process exits
		if pid:
			return 0

		# 1st child process becomes session leader
		os.setsid()

		# fork again, relinquish terminal forever
		pid = os.fork()
		# 1st child exits
		if pid:
			return 1

		# child process is now a daemon, set cwd and umask
		os.chdir("/")
		os.umask(0077)

		# close default stdin/out/err
		os.close(sys.stdout.fileno())
		os.close(sys.stderr.fileno())
		os.close(sys.stdin.fileno())

		# open new stdin/out/err
		outfile = open(raw_output_log, "a", 1)
		sys.stdout = outfile
		sys.stderr = outfile
		sys.stdin = open('/dev/null')

		# write pid file
		self.set_pid()

		print "STARTING DAEMON '%s' (%s)" % (self.name, time.ctime())
		# run the daemon
		try:
			start_fn(**start_params)
		except Exception as e:
			print "ERROR WHILE RUNNING '%s'" % self.name
			traceback.print_exc()

		# when second child is complete, remove pid file
		self.unset_pid()

		print "EXITED DAEMON '%s' (%s)" % (self.name, time.ctime())
		return 2
