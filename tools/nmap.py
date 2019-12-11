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
