"""
Made By: Russian Otter

Romap is a Network Scanning
Utility coded in python and
made for Pythonista!
This application allows the
user to preform fast, detailed
scans on their or other's networks 
and or subnets! Created by
Russian Otter in SavSec / Savage 
Security, Romap was made from
scratch and has built up to be
the effective program it is today!
The earily versions of this
program were slow and did
simple ip discovery, but now
Romap has been through tons
of changes and has gained tons
of commands and abilities that
make the program even more user
friendly! Commands are simple and
optional which allows the usage
of this program to be extremely easy!

-=-=-=- MIT License -=-=-=-

Copyright (c) 2017 SavSec

Permission is hereby granted,
free of charge, to any person
obtaining a copy of this
software and associated
documentation files (the
"Software"), to deal in
the Software without restriction, 
including without limitation
the rights to use, copy,
modify, merge, publish, distribute, 
sublicense, and/or sell
copies of the Software,
and to permit persons to whom the
Software is furnished to do so,
subject to the following
conditions:

The above copyright notice
and this permission notice
shall be included in all
copies or substantial portions
of the Software.

THE SOFTWARE IS PROVIDED
"AS IS", WITHOUT WARRANTY OF
ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT
LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR
A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT
SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE
USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import sys, console, time, socket, random, string, sys, uuid, random, urllib2, argparse, ssl, os, inspect, re
from datetime import datetime
from urllib2 import urlopen
from datetime import timedelta
from objc_util import *

parser = argparse.ArgumentParser()
parser.add_argument("-s","--ssl",help="Grabs SSL Certificates", action="store_true")
parser.add_argument("-l","--log",help="Logs scan to file")
parser.add_argument("-a","--accesspoint",help="Locate access points", action="store_true")
parser.add_argument("-p","--public",help="Scan Public Addresses",type=str,default="")
parser.add_argument("-d","--detail",help="Device Detail Information", action="store_true")
parser.add_argument("-H","--Host",help="Scan Selective Target")
parser.add_argument("-P","--Range",help="Port Range For -H",default="500")
parser.add_argument("-t","--timeout",help="Set timeout",default=2,type=int)
parser.add_argument("-D","--Direct",help="Directly Scan Device",default="",type=str)
parser.add_argument("-m","--mid",help="Second IP Range [17-62]",default="None")
parser.add_argument("-M","--Mid",help="Third IP Range [17-62]",default="None")
parser.add_argument("-n","--nohelp",help="Hides Autohelp",action="store_true")
parser.add_argument("-S","--Search",help="Search For Port While Scanning\n\n",type=int)
args = parser.parse_args()
__author__ = "RussianOtter"
__status__ = "Finished"
__version__ = "v3.4.7"

if not args.log or not args.Host:
	print ""
	console.set_font("Menlo",11.4)
	if args.nohelp:
		pass
	else:
		parser.print_help()
		print "Examples:\nromap.py -n -d -s -m 1-13 -t 1 -l log.txt\nromap.py -H 192.168.1.254 -P 1000\nromap.py -n"
	console.set_font()
	time.sleep(2)

sl = args.ssl
log = args.log
acp = args.accesspoint
dtl = args.detail
hst = args.Host
rng = args.Range
tot = args.timeout
srng = args.mid
dv = args.Direct
prt = args.Search

srch = False
if len(str(args.Search)) > 0:
	srch = True

try:
	if len(args.public) > 1:
		console.set_color(1,0,0)
		print "Warning: Scanning Public IPs may appear as an attack to the hosts being scanned!"
		time.sleep(3)
		console.set_font()
except:
	pass

socket.setdefaulttimeout(tot)

ssdpsrc = { "ip_address" : "239.255.255.250",
"port" : 1900,
"mx"   : 10,
"st"   : "ssdp:all" }

exptpack1 = """M-SEARCH * HTTP/1.1
HOST: {ip_address}:{port}
MAN: "ssdp:discover"
ST: uuid:`reboot`
MX: 2
""".replace("\n", "\r\n").format(**ssdpsrc) + "\r\n"

ssdpre = """M-SEARCH * HTTP/1.1
HOST: {ip_address}:{port}
MAN: "ssdp:discover"
MX: {mx}
ST: {st}
""".replace("\n", "\r\n").format(**ssdpsrc) + "\r\n"

def discover(match="", timeout=2):
	"""
	The discover code is
	used when searching for
	upnp devices! UPnP scanning
	can allow you to find
	vulnerable devices on the
	network!
	"""
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	s.sendto(ssdpre, (ssdpsrc["ip_address"], ssdpsrc["port"]))
	s.settimeout(tot)
	responses = []
	print ""
	try:
		while True:
			response = s.recv(1000)
			if match in response:
				print response
				if len(log) > 2:
					f = open(log,"a")
					f.write(response)
					f.close()
				responses.append(response)
	except:
		pass
	return responses

def pinger_urllib(host):
	"""
	Simple urllib ping test
	"""
	t1 = time.time()
	try:
		urllib2.urlopen(host, timeout=3)
		elapsed_time = time.time() - t1
		timesq = str(timedelta(seconds=elapsed_time))
		return (timesq)
	except:
		pass

def deepscan(target):
	"""
	DeepScan is a verbose
	tool used to gather more
	information about a device!
	"""
	data = str(socket.gethostbyaddr(target))
	data = data.replace(",","").replace("[","").replace("]","").replace("(","").replace(")","").replace("'","")
	data = data.split()
	print "-Name:",data[0]
	print "-FQDN:",data[1]
	print "-Provider:",data[2]
	try:
		ping = pinger_urllib("http://" + target)
		print "-HTTP Response:",ping,"ms"
		if len(log) > 2:
			f = open(log,"a")
			f.write("\n-Name:"+data[0] + "\n")
			f.write("-FQDN:"+data[1] + "\n")
			f.write("-Provider:"+data[2] + "\n")
	except:
		pass

def sslc(host):
	"""
	This is the basic
	function used to grab
	ssl certificates from
	devices on the network
	which have ssl setup!
	You can activate
	this function with
	the argument: -S
	"""
	try:
		s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		host = host.replace("http://","")
		s.connect((host,443))
		temp = ssl.get_server_certificate((host,443))
		print "-Has Certificate"
		s.close()
		if len(log) > 2:
			f = open(log,"a")
			f.write("\n" + temp + "\n")
			f.close()
	except:
		pass

def credits():
	"""
	Copyright (c) Romap v3.4.7 - SavSec
	"""
	console.set_color(1,1,0)
	print "   _ __ ___  _ __ ___   __ _ _ __ "
	print "  | '__/ _ \| '_ ` _ \ / _` | '_ \ "
	print "  | | | (_) | | | | | | (_| | |_)| "
	print "  |_|  \___/|_| |_| |_|\__,_| .__/"
	print "                            |_|   "
	console.set_color()
	print " " * 2 + "Starting romap on %s\n" %(socket.gethostname())
	time.sleep(1)

def scanport(target):
	"""
	This is the port scanner
	for Romap! You can change
	the maxium amount of ports
	to scan with the argument:
	-P [Max Port]
	"""
	t1 = datetime.now()
	print "Scanning: "+target+":1-"+rng
	try:
		for port in range(1,int(rng)+1):
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			result = s.connect_ex((target, port))
			time.sleep(0.03)
			if result == 0:
				print "Port {}: Open".format(port)
			s.close()
	except KeyboardInterrupt:
		print "Received Ctrl+C"
		sys.exit()
	except socket.gaierror:
		print "Hostname could not be resolved. Exiting"
		sys.exit()
	except socket.error:
		print "Couldn't connect to server"
		sys.exit()
	t2 = datetime.now()
	total =  t2 - t1
	print "Scanning Complete ", total
	sys.exit()

try:
	if len(args.Direct) > 1:
		deepscan(dv)
		scanport(dv)
except:
	sys.exit()

def romap():
	"""
	This is the main script
	inside Romap that processes
	the scans and controls the
	outputs. One of the most 
	useful peices of code inside
	this script, allows ip
	addresses to be clicked
	on after scanning. When 
	the ip is clicked romap will
	run a scan on that ip!
	"""
	path1 = os.path.abspath(inspect.stack()[0][1])
	path1 = re.sub(r'.*ents/', '', path1)
	path1 = "pythonista3://" + path1
	path1 = path1.replace("<string>","")
	path1 = path1.replace("romap.py","romap.py?action=run&argv=-n&argv=-P&argv=")
	path1 = path1 + rng + "&argv=-t&argv=" + str(tot) + "&argv=-D&argv="
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("google.com", 80))
	host = s.getsockname()[0]
	lan = host
	try:
		my_ip = "N/A"
		my_ip = urlopen('http://ip.42.pl/raw').read()
	except:
		pass
	if len(my_ip) > 18:
		my_ip = 'N/A'
	macaddr = hex(uuid.getnode()).replace('0x', '').upper()
	mac = ':'.join(macaddr[i : i + 2] for i  in range(0,	11, 2))
	time.sleep(0.4)
	print "LAN: %s" %(lan)
	time.sleep(0.4)
	print "MAC: %s" %(mac)
	time.sleep(0.4)
	print "PUB: %s" %(my_ip)
	time.sleep(0.4)
	CNCopyCurrentNetworkInfo = c.CNCopyCurrentNetworkInfo
	CNCopyCurrentNetworkInfo.restype = c_void_p
	CNCopyCurrentNetworkInfo.argtypes = [c_void_p]
	wifiid = ObjCInstance(CNCopyCurrentNetworkInfo(ns('en0')))
	print "SSID: %s" %(wifiid["SSID"])
	time.sleep(0.4)
	print "BSSID: %s" %(wifiid["BSSID"])
	time.sleep(0.4)
	print(uuid.uuid5(uuid.NAMESPACE_DNS, "0.0.0.0"))
	time.sleep(0.4)
	byte = random._urandom(16)
	print(uuid.UUID(bytes=byte))
	time.sleep(0.4)
	print(uuid.uuid4())
	time.sleep(0.4)
	print(uuid.uuid3(uuid.NAMESPACE_DNS, "0.0.0.0"))
	time.sleep(0.4)
	print(uuid.uuid1())
	time.sleep(0.4)
	byte = random._urandom(16)
	print(uuid.UUID(bytes=byte))
	time.sleep(0.4)
	print ""
	s.close()
	start_time = time.time()
	try:
		if len(args.public) > 1:
			host = args.public
	except:
		pass
	host = host.split(".")
	bkmid = host[2]
	host[3] = "%s"
	host[2] = "%s"
	if args.Mid != "None":
		host[1] = "%s"
	host = ".".join(host)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	network = str(host)
	td = 0
	if args.mid != "None" and args.Mid != "None":
		srng = args.mid.split("-")
		srng2 = args.Mid.split("-")
		for tend in range(int(srng2[0]),int(srng2[1])+1):
			for mend in range(int(srng[0]),int(srng[1])+1):
				for end in range(256):
					ip = network % (tend,mend,end)
					try:
						info = socket.gethostbyaddr(ip)
						info2 = 	str(info[2]).replace("[","").replace("]","").replace("'","")
						info3 = info[0]+" -- "
						sys.stdout.write(info3)
						console.write_link(info2,path1+info2)
						td = td + 1
						print ""
						try:
							if len(log) > 2:
								f = open(log,"a")
								f.write(str(info[0])+" -- "+str(info2)+ "\n")
						except:
							pass
						if srch:
							s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
							result = s.connect_ex((info2, prt))
							if result == 0:
								print "Port {}: Open".format(prt)
							s.close()
						if sl:
							sslc(info2)
						try:
							if dtl:
								deepscan(info2)
								time.sleep(0.05)
						except:
							pass
					except:
						pass
	
	if args.mid == "None":
		for end in range(256):
			ip = network % (bkmid,end)
			try:
				info = socket.gethostbyaddr(ip)
				info2 = 	str(info[2]).replace("[","").replace("]","").replace("'","")
				info3 = info[0]+" -- "
				sys.stdout.write(info3)
				console.write_link(info2,path1+info2)
				td = td + 1
				print ""
				if srch:
					s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					result = s.connect_ex((info2, prt))
					if result == 0:
						print "Port {}: Open".format(prt)
					s.close()
				try:
					if len(log) > 2:
						f = open(log,"a")
						f.write(str(info[0])+" -- "+str(info2)+ "\n")
				except:
					pass
				if sl:
					sslc(info2)
				try:
					if dtl:
						deepscan(info2)
						time.sleep(0.05)
				except:
					pass
			except:
				pass
	if args.mid != "None" and args.Mid == "None":
		srng = args.mid.split("-")
		for mend in range(int(srng[0]),int(srng[1])+1):
			for end in range(256):
				ip = network % (mend,end)
				try:
					info = socket.gethostbyaddr(ip)
					info2 = 	str(info[2]).replace("[","").replace("]","").replace("'","")
					info3 = info[0]+" -- "
					sys.stdout.write(info3)
					console.write_link(info2,path1+info2)
					td = td + 1
					print ""
					if srch:
						s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
						result = s.connect_ex((info2, prt))
						if result == 0:
							print "Port {}: Open".format(prt)
						s.close()
					try:
						if len(log) > 2:
							f = open(log,"a")
							f.write(str(info[0])+" -- "+str(info2)+ "\n")
					except:
						pass
					if sl:
						sslc(info2)
					try:
						if dtl:
							deepscan(info2)
							time.sleep(0.05)
					except:
						pass
				except:
					pass
	print ""
	elapsed_time = time.time() - start_time
	time.sleep(0.5)
	times = str(timedelta(seconds=elapsed_time))
	sys.stdout.write("Time Elapsed: ")
	sys.stdout.write(str(times))
	print "\nTotal Device(s) Found:",td
	try:
		if acp:
			print "\n"
			discover()
	except:
		pass

credits()
try:
	if len(hst) > 0:
		scanport(hst)
except:
	pass
romap()
