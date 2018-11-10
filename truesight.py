import os
import subprocess
import xml.etree.ElementTree as ET
from collections import defaultdict

#maybe just run a targetted nmap scan on things like port 80... but what if http service found on diff port?
#start out with just full scan I guess

#base_folder = "/root/htb/ACTIVE"

#define a machine object?

ctf_machine = "test"
ctf_ip = "10.10.10.102"

base_folder = "/root/code/python/tmp/" + ctf_machine + "/scans/"

def buildDir(path):
	try:
		os.makedirs(path)
	except Exception as e:
		pass
		#print "Dir already exists"

def callProcess(command):
	print command
	#print command.split(" ")
	#subprocess.call(command)

def http_runbook(ports):

	local_log = ""

	#maybe tool_process function since theyre pretty similar

	for port in ports:
		#run nikto

		local_log = base_folder + "nikto/" + ctf_machine + ".txt"

		buildDir(base_folder + "nikto")
		callProcess("nikto -host " + ctf_ip + " -port " + port + " -output " + local_log)

		#run gobuster

		local_log = base_folder + "gobuster/" + ctf_machine + ".txt"

		user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
		wordlist = "/usr/share/wordlists/dirbuster/directory-list-2.3-small.txt"

		buildDir(base_folder + "gobuster")
		callProcess("gobuster -u http://" + ctf_ip + " -w " + wordlist + " -a \"" + user_agent + "\" -o " + local_log)

		#add -x gobuster for file types based on webserver



buildDir(base_folder + "nmap")

#subprocess.call(["nmap","-sV","-p", "20-81","-T4","-oA", base_folder + ctf_machine + "/scans/nmap/" + ctf_machine, ctf_ip])
callProcess("nmap -sV -p 20-81 -T4 -oA " + base_folder + "scans/nmap/" + ctf_machine + " " + ctf_ip)

e = ET.parse("/root/htb/FINISHED/hawk/scans/nmap/hawk.xml")
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
http_runbook(services["http"])

	#for service in port.find("service"):
		



#for service in scaninfo.iter("services"):
#	print service
