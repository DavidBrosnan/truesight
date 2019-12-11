from abc import ABCMeta, abstractmethod

class Tool:

	__metaclass__ = ABCMeta

	def __init__(self):

		self.name = "Default"
		self.dir_path = "/default/path/to/tool"
		self.tool_out = "tool_output.txt"
		self.command_out = "ts_command_output.txt" #add command string to first line of this output
		self.ports = []

	@abstractmethod
	def execute(self):
		#Steps for execution of the actual tool
		pass

	@abstractmethod
	def setup(self):
		#Steps for building directories, dependent files exist, etc.
		pass




