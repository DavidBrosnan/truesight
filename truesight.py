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


def http_runbook(target_machine, target_ip, ports):

	local_log = ""

	tools = ["nikto","gobuster","wget"]

	for tool in tools:
		os_inf.build_dir(os_inf.BASE_FOLDER + tool)


	for port in ports:
		#run nikto

		local_log = os_inf.BASE_FOLDER + "nikto/" + port + "/" + ctf_machine + ".txt"
		command_log = os_inf.BASE_FOLDER + "nikto/" + port + "/command_log.txt"

		os_inf.build_dir(os_inf.BASE_FOLDER + "nikto/" + port)
		os_inf.call_process("nikto -host " + ctf_ip + " -port " + port + " -output " + local_log, command_log)

		#run gobuster

		local_log = os_inf.BASE_FOLDER + "gobuster/" + port + "/" + ctf_machine + ".txt"
		command_log = os_inf.BASE_FOLDER + "gobuster/" + port + "/command_log.txt"

		#avoid devices that observe user-agent filtering
		user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
		wordlist = "/usr/share/wordlists/dirbuster/directory-list-2.3-small.txt"

		os_inf.build_dir(os_inf.BASE_FOLDER + "gobuster/" + port)
		os_inf.call_process("gobuster -u http://" + ctf_ip + " -w " + wordlist + " -a \"" + user_agent + "\" -o " + local_log, command_log)

		#run wget

		local_log = os_inf.BASE_FOLDER + "wget/" + port + "/" + ctf_machine + ".txt"
		command_log = os_inf.BASE_FOLDER + "wget/" + port + "/command_log.txt"

		os_inf.build_dir(os_inf.BASE_FOLDER + "wget/" + port)
		os_inf.call_process("wget --recursive --level 3 -o " + local_log + " -P " + os_inf.BASE_FOLDER + "wget/" + port + " " + ctf_ip, command_log)

def main(target_machine, target_ip):
	
	os_inf.BASE_FOLDER = "/root/tmp/ts/" + target_machine + "/scans/"
	os_inf.TARGET_NAME = target_machine
	os_inf.TARGET_IP = target_ip
	
	scanner = toolbox.Nmap()
	print scanner.execute()

	#print services["http"]

	return

	http_runbook(ctf_machine, ctf_ip, services["http"])


if __name__ == "__main__":

	main(sys.argv[1],sys.argv[2])



