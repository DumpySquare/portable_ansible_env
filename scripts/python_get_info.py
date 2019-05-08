#/usr/bin/python

from os import system;
from socket import gethostname;
print gethostname()
print system("uptime")
print system("tmsh show sys version")

