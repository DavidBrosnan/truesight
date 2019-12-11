from modules import tool
from modules import os_inf

import xml.etree.ElementTree as ET
from collections import defaultdict


class Wget(tool.Tool):

	def __init__(self, ports):
		tool.Tool.__init__(self)
		self.name = "wget"
		#repeat dir_path piece, can probably put into base class
		self.dir_path = os_inf.BASE_FOLDER + "wget/"
		self.ports = ports
		self.setup()
		#self.URI = 

	def execute(self):

		for port in self.ports:
			port_path = self.dir_path + port + "/"
			os_inf.call_process("wget --recursive --level 3 -o " + port_path + self.tool_out + " -P " + port_path + " " + os_inf.TARGET_IP, port_path, self.command_out)
			#html_comments(port_path)
			#robots(port_path)

	def setup(self):
		#fix this to work with multiple ports
		for port in self.ports:
			os_inf.build_dir(os_inf.BASE_FOLDER + "wget/" + port)

	def html_comments(self, port_path):
		os_inf.call_process("grep \"password\" -r " + port_path + " -f " + port_path + "password_grep")

	def robots(self, port_path):
		#what if site has base url thats not root dir? can we detect that?
		os_inf.call_process("wget -o " + port_path + self.tool_out + " -P " + port_path + " " + os_inf.TARGET_IP + "/robots.txt")