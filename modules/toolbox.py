from modules import tool
from modules import os_inf

import xml.etree.ElementTree as ET
from collections import defaultdict

class Nmap(tool.Tool):

	def __init__(self):
		tool.Tool.__init__(self)
		self.name = "nmap"
		self.setup()

	def execute(self, nmap_import):
		
		#os_inf.call_process("nmap -sV -sC -p- -T4 -oA " + os_inf.BASE_FOLDER + "nmap/" + os_inf.TARGET_NAME + " " + os_inf.TARGET_IP, self.command_log,True)


		if nmap_import is None:
			os_inf.call_process("sudo nmap -sV -sC -p- -T4 -oA " + os_inf.BASE_FOLDER + "nmap/" + os_inf.TARGET_NAME + " " + os_inf.TARGET_IP, os_inf.BASE_FOLDER + "nmap/", self.command_out,True)
			e = ET.parse(os_inf.BASE_FOLDER + "nmap/" + os_inf.TARGET_NAME + ".xml")
		
		else:
			e = ET.parse(nmap_import)	


		root = e.getroot()

		ports = root.find("host").find("ports")

		services = {}

		#so every key has a default value of a list
		services = defaultdict(lambda: [], services)

		for port in ports.iter("port"):

			service = port.find("service")

			if service is not None:			
				service_name = port.find("service").attrib['name']
				portid = port.attrib['portid']

				services[service_name].append(portid)

		return services

	def setup(self):
		
		#Build directory
		os_inf.build_dir(os_inf.BASE_FOLDER + "nmap")




class Nikto(tool.Tool):

	def __init__(self, ports):
		tool.Tool.__init__(self)
		self.name = "nikto"
		self.dir_path = os_inf.BASE_FOLDER + "nikto/"
		self.ports = ports
		self.setup()

	def execute(self):

		for port in self.ports:

			port_path = self.dir_path + port + "/"

			os_inf.call_process("sudo nikto -host " + os_inf.TARGET_IP + " -port " + port + " -output " + port_path + self.tool_out, port_path, self.command_out)

	def setup(self):
		for port in self.ports:
			os_inf.build_dir(os_inf.BASE_FOLDER + "nikto/" + port)



class Gobuster(tool.Tool):

	def __init__(self, ports):
		tool.Tool.__init__(self)
		self.name = "gobuster"
		self.dir_path = os_inf.BASE_FOLDER + "gobuster/"
		self.ports = ports
		self.setup()

	def execute(self):

		user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
		wordlist = "/usr/share/wordlists/dirbuster/directory-list-2.3-small.txt"

		for port in self.ports:
			port_path = self.dir_path + port + "/"

			os_inf.call_process("sudo gobuster dir -u http://" + os_inf.TARGET_IP + ":" + port + " -w " + wordlist + " -a \"" + user_agent + "\" -o " + port_path + self.tool_out, port_path, self.command_out)

	def setup(self):
		#fix this to work with multiple ports
		for port in self.ports:
			os_inf.build_dir(os_inf.BASE_FOLDER + "gobuster/" + port)



class Wget(tool.Tool):

	def __init__(self, ports):
		tool.Tool.__init__(self)
		self.name = "wget"
		#repeat dir_path piece, can probably put into base class
		self.dir_path = os_inf.BASE_FOLDER + "wget/"
		self.ports = ports
		self.setup()
		#self.URI = 

	#move this function up
	def html_comments(self, port_path):
		os_inf.call_process("grep \"password\" -r " + port_path + " -f " + port_path + "password_grep", port_path, self.command_out)

	def execute(self):

		for port in self.ports:
			port_path = self.dir_path + port + "/"
			os_inf.call_process("sudo wget --recursive --level 3 -o " + port_path + self.tool_out + " -P " + port_path + " " + os_inf.TARGET_IP, port_path, self.command_out)
			self.html_comments(port_path)
			self.robots(port_path)

	def setup(self):
		#fix this to work with multiple ports
		for port in self.ports:
			os_inf.build_dir(os_inf.BASE_FOLDER + "wget/" + port)



	def robots(self, port_path):
		#what if site has base url thats not root dir? can we detect that?
		os_inf.call_process("sudo wget -o " + port_path + self.tool_out + " -P " + port_path + " " + os_inf.TARGET_IP + "/robots.txt", port_path, self.command_out)
