from modules import tool
from modules import os_inf

import xml.etree.ElementTree as ET
from collections import defaultdict


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