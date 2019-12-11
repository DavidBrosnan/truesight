import os
import errno
import subprocess
import sys
import ConfigParser


from modules import os_inf
from modules import tool
#from modules import toolbox
from tools import *
#import tools


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

	toolbox = []

	toolbox.append(nikto.Nikto(ports))
	toolbox.append(gobuster.Gobuster(ports))
	toolbox.append(wget.Wget(ports))

	for tool in toolbox:
		tool.execute()

	return

def main(target_machine, target_ip, nmap_file=None):

	config = ConfigParser.ConfigParser()
	config.read('config.ini')

	base = config.get('Properties', 'base')
	
	os_inf.BASE_FOLDER = base + target_machine + "/scans/"
	os_inf.TARGET_NAME = target_machine
	os_inf.TARGET_IP = target_ip
	
	scanner = nmap.Nmap()
	services = scanner.execute(nmap_file)

	#print services["http"]
	http_runbook(services["http"])


if __name__ == "__main__":

	if len(sys.argv) > 3:
			main(sys.argv[1],sys.argv[2],sys.argv[3])
	else:
		main(sys.argv[1],sys.argv[2])



