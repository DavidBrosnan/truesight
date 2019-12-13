import os
import errno
import subprocess

#Add a process to check for PIDs spawned by this script and optionally dont finish until all PIDS closed.

BASE_FOLDER = ""
TARGET_NAME = ""
TARGET_IP = ""

def build_dir(path):
	try:
		os.makedirs(path)
	except OSError as e:
		if e.errno == errno.EEXIST:
			pass
			#print "Directory " + path + " already exists"
		else:
			raise

def call_process(command, path, outfile, if_wait=False):
	print(command)
	
	outfile = open(path + "/" + outfile,"w")
	process = subprocess.Popen(command.split(" "), stdout=outfile, stderr=outfile)

	print("Process PID:  " + str(process.pid))

	if if_wait:
		print("WAITING PROCESS...")
		process.wait()


	


	