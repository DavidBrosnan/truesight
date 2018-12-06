import os
import errno
import subprocess
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict

from lib.modules import os_inf
from lib.modules import tool

from lib.tools import *

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


def http_runbook(base_folder, ctf_machine, ctf_ip, ports):

	local_log = ""

	tools = ["nikto","gobuster","wget"]

	for tool in tools:
		os_inf.build_dir(base_folder + tool)


	for port in ports:
		#run nikto

		local_log = base_folder + "nikto/" + port + "/" + ctf_machine + ".txt"
		command_log = base_folder + "nikto/" + port + "/command_log.txt"

		os_inf.build_dir(base_folder + "nikto/" + port)
		os_inf.call_process("nikto -host " + ctf_ip + " -port " + port + " -output " + local_log, command_log)

		#run gobuster

		local_log = base_folder + "gobuster/" + port + "/" + ctf_machine + ".txt"
		command_log = base_folder + "gobuster/" + port + "/command_log.txt"

		#avoid devices that observe user-agent filtering
		user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
		wordlist = "/usr/share/wordlists/dirbuster/directory-list-2.3-small.txt"

		os_inf.build_dir(base_folder + "gobuster/" + port)
		os_inf.call_process("gobuster -u http://" + ctf_ip + " -w " + wordlist + " -a \"" + user_agent + "\" -o " + local_log, command_log)

		#run wget

		local_log = base_folder + "wget/" + port + "/" + ctf_machine + ".txt"
		command_log = base_folder + "wget/" + port + "/command_log.txt"

		os_inf.build_dir(base_folder + "wget/" + port)
		os_inf.call_process("wget --recursive --level 3 -o " + local_log + " -P " + base_folder + "wget/" + port + " " + ctf_ip, command_log)

def run(ctf_machine, ctf_ip):
	
	base_folder = "/root/htb/ACTIVE/" + ctf_machine + "/scans/"

	os_inf.build_dir(base_folder + "nmap")

	command_log = base_folder + "nmap/truesight_command_log.txt"
	os_inf.call_process("nmap -sV -sC -p- -T4 -oA " + base_folder + "nmap/" + ctf_machine + " " + ctf_ip, command_log,True)

	e = ET.parse(base_folder + "nmap/" + ctf_machine + ".xml")
	root = e.getroot()

	ports = root.find("host").find("ports")

	services = {}

	#so every key has a default value of a list
	services = defaultdict(lambda: [], services)

	for port in ports.iter("port"):
		service_name = port.find("service").attrib['name']
		portid = port.attrib['portid']

		services[service_name].append(portid)


	print services["http"]
	http_runbook(base_folder, ctf_machine, ctf_ip, services["http"])


if __name__ == "__main__":

	run(sys.argv[1],sys.argv[2])



