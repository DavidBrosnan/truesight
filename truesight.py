import os
import subprocess
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict

"""
Tools required:

	nmap
	nikto
	gobuster
	wget


"""
#eventually read from a config file instead of here

#check if nmap logs already exist

#Consider an --init function to setup folder structure?
# --Reset function to restart from scratch


#trueisght machine_name machine_ip [runbook]
#force reset option

#add automatic entry to /etc/hosts file?

#define a machine object?


def build_dir(path):
	try:
		os.makedirs(path)
	except Exception as e:
		pass
		#print "Dir already exists"

def call_process(command, outfile_path, if_wait=False):
	print command
	
	outfile = open(outfile_path,"w")
	process = subprocess.Popen(command.split(" "), stdout=outfile, stderr=outfile)

	if if_wait:
		print "WAITING PROCESS..."
		process.wait()

def tool_execute(name, *args):
	pass

#def ssh_runbook(ports):
#def ftp_runbook(ports):
	#anonymous login
#def dns_runbook(ports):
	#zone transfer


def http_runbook(base_folder, ctf_machine, ctf_ip, ports):

	local_log = ""

	#maybe tool_process function since theyre pretty similar

	tools = ["nikto","gobuster","wget"]

	for tool in tools:
		build_dir(base_folder + tool)


	for port in ports:
		#run nikto

		local_log = base_folder + "nikto/" + port + "/" + ctf_machine + ".txt"
		command_log = base_folder + "nikto/" + port + "/command_log.txt"

		#build_dir(base_folder + "nikto")
		build_dir(base_folder + "nikto/" + port)
		call_process("nikto -host " + ctf_ip + " -port " + port + " -output " + local_log, command_log)

		#run gobuster

		local_log = base_folder + "gobuster/" + port + "/" + ctf_machine + ".txt"
		command_log = base_folder + "gobuster/" + port + "/command_log.txt"

		#avoid devices that observe user-agent filtering
		user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
		wordlist = "/usr/share/wordlists/dirbuster/directory-list-2.3-small.txt"

		#build_dir(base_folder + "gobuster")
		build_dir(base_folder + "gobuster/" + port)
		call_process("gobuster -u http://" + ctf_ip + " -w " + wordlist + " -a \"" + user_agent + "\" -o " + local_log, command_log)

		#sqlmap?


		#grab robots.txt AND see which ones respond
		#show all html comments for all 200's in the directory bruteforce/
		#Use Wget for this?
		local_log = base_folder + "wget/" + port + "/" + ctf_machine + ".txt"
		command_log = base_folder + "wget/" + port + "/command_log.txt"

		#build_dir(base_folder + "wget")
		build_dir(base_folder + "wget/" + port)
		call_process("wget --recursive --level 3 -o " + local_log + " -P " + base_folder + "wget/" + port + " " + ctf_ip, command_log)



		#add -x gobuster for file types based on webserver

def run(ctf_machine, ctf_ip):

	base_folder = "/root/htb/ACTIVE/" + ctf_machine + "/scans/"

	build_dir(base_folder + "nmap")

	#subprocess.call(["nmap","-sV","-p", "20-81","-T4","-oA", base_folder + ctf_machine + "/scans/nmap/" + ctf_machine, ctf_ip])
	command_log = base_folder + "nmap/truesight_command_log.txt"
	call_process("nmap -sV -sC -p- -T4 -oA " + base_folder + "nmap/" + ctf_machine + " " + ctf_ip, command_log,True)

	#e = ET.parse("/root/htb/FINISHED/hawk/scans/nmap/hawk.xml")
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

	#for service in port.find("service"):


#for service in scaninfo.iter("services"):
#	print service


if __name__ == "__main__":

	run(sys.argv[1],sys.argv[2])



