import sys, console, time, socket, random, string, sys, uuid, random, threading, urllib2
from urllib2 import urlopen
from datetime import timedelta

def pinger_urllib(host):
	t1 = time.time()
	try:
		urllib2.urlopen(host, timeout=3)
		return (time.time() - t1) * 1000.0
	except:
		pass

def deepscan(target="192.168.1.254"):
	data = str(socket.gethostbyaddr(target))
	data = data.replace(",","").replace("[","").replace("]","").replace("(","").replace(")","").replace("'","")
	data = data.split()
	print "-Name:",data[0]
	print "-FQDN:",data[1]
	print "-Provider:",data[2]
	try:
		ping = pinger_urllib("http://" + target)
		print "-HTTP Response:",ping
	except:
		pass
	print ""

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
	host[3] = str(0)
	host = ".".join(host)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	network = str(host)
	for end in range(256):
		ip = network + str(end)
		try:
			info = socket.gethostbyaddr(ip)
			info2 = str(info[2]).replace("[","").replace("]","").replace("'","")
			print info[0], "--", info2
			try:
				if sys.argv[1] == "-d":
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
	print "\n"
def netstat():
	print "In Progress"
credits()
romap()
#netstat()
