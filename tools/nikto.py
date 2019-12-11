from modules import tool
from modules import os_inf

import xml.etree.ElementTree as ET
from collections import defaultdict


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
