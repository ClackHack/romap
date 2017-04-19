import sys, console, time, socket, random, string, sys, uuid, random, urllib2, argparse, ssl
from datetime import datetime
from urllib2 import urlopen
from datetime import timedelta

parser = argparse.ArgumentParser()
parser.add_argument("-s","--ssl",help="Grabs SSL Certificates", action="store_true")
parser.add_argument("-l","--log",help="Logs scan to file")
parser.add_argument("-a","--accesspoint",help="Locate access points", action="store_true")
parser.add_argument("-d","--detail",help="Device Detail Information", action="store_true")
parser.add_argument("-H","--Host",help="Scan Selective Target")
parser.add_argument("-R","--Range",help="Port Range For -H",default="500")
parser.add_argument("-t","--timeout",help="Set timeout",default=2,type=int)
parser.add_argument("-m","--mid",help="Second IP Range 0.0.x.0",default=1,type=int)
parser.add_argument("-n","--nohelp",help="Hides Autohelp\n",action="store_true")
args = parser.parse_args()

if not args.log or not args.Host:
	print ""
	console.set_font("Menlo",11.4)
	if args.nohelp:
		pass
	else:
		parser.print_help()
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
	t1 = time.time()
	try:
		urllib2.urlopen(host, timeout=3)
		return (time.time() - t1) * 1000.0
	except:
		pass

def deepscan(target):
	data = str(socket.gethostbyaddr(target))
	data = data.replace(",","").replace("[","").replace("]","").replace("(","").replace(")","").replace("'","")
	data = data.split()
	print "-Name:",data[0]
	print "-FQDN:",data[1]
	print "-Provider:",data[2]
	try:
		ping = pinger_urllib("http://" + target)
		print "-HTTP Response:",ping
		if len(log) > 2:
			f = open(log,"a")
			f.write("\n-Name:"+data[0] + "\n")
			f.write("-FQDN:"+data[1] + "\n")
			f.write("-Provider:"+data[2] + "\n")
	except:
		pass
	print ""

def sslc(host):
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
	t1 = datetime.now()
	print "Scanning: "+target+":1-"+rng+"\n"
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
	print "\nScanning Complete ", total
	sys.exit()

def romap():
	start_time = time.time()
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
	print "RTT: %s" %("0.0.0.0")
	time.sleep(0.4)
	print "MAC: %s" %(mac)
	time.sleep(0.4)
	print "PUB: %s" %(my_ip)
	time.sleep(0.4)
	print(uuid.uuid5(uuid.NAMESPACE_DNS, "0.0.0.0"))
	time.sleep(0.6)
	byte = random._urandom(16)
	print(uuid.UUID(bytes=byte))
	time.sleep(0.6)
	print(uuid.uuid4())
	time.sleep(0.6)
	print(uuid.uuid3(uuid.NAMESPACE_DNS, "0.0.0.0"))
	time.sleep(0.6)
	print(uuid.uuid1())
	time.sleep(0.6)
	byte = random._urandom(16)
	print(uuid.UUID(bytes=byte))
	time.sleep(0.8)
	print ""
	s.close()
	host = host.split(".")
	host[3] = "%s"
	host[2] = "%s"
	host = ".".join(host)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	network = str(host)
	for mend in range(srng):
		for end in range(256):
			ip = network % (srng,end)
			try:
				info = socket.gethostbyaddr(ip)
				info2 = 	str(info[2]).replace("[","").replace("]","").replace("'","")
				print info[0], "--", info2
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
