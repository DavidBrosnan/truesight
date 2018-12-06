

from lib.modules import tool
from lib.tools import nmap

n = nmap.Nmap()

print n.name
print n.tool_out
print n.command_out
