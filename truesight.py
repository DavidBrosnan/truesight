import os
import errno
import subprocess
import sys

from lib.modules import os_inf
from lib.modules import tool
from lib.modules import toolbox

"""
Tools required:

	nmap
	nikto
	gobuster
	wget


"""
#def ssh_runbook(ports):
#def ftp_runbook(ports):
	#anonymous login
#def dns_runbook(ports):
	#zone transfer


def http_runbook(ports):

	local_log = ""

	tools = []

	tools.append(toolbox.Nikto(ports))
	tools.append(toolbox.Gobuster(ports))
	tools.append(toolbox.Wget(ports))

	for tool in tools:
		tool.execute()

	return

def main(target_machine, target_ip):
	
	os_inf.BASE_FOLDER = "/root/tmp/ts/" + target_machine + "/scans/"
	os_inf.TARGET_NAME = target_machine
	os_inf.TARGET_IP = target_ip
	
	scanner = toolbox.Nmap()
	services = scanner.execute()

	#print services["http"]
	http_runbook(services["http"])


if __name__ == "__main__":

	main(sys.argv[1],sys.argv[2])



