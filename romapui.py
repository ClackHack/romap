import socket, threading, sys, time, ui
from datetime import timedelta

ctime = str(timedelta(seconds = time.time())).split(", ")[1][:11]
socket.setdefaulttimeout(0)
stop = True
time.sleep(0.5)
stop = False
network = ""
router = "[*]\nRouter"
ips = []

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	localip = s.getsockname()[0]
	s.close()
	d1 = ".".join(localip.split(".")[:3])
	d1,d2 = d1+".1",d1+".254"
	localip = "[+]\n"+localip
except:
	d1,d2 = "8.8.4.4\n8.8.8.25".split("\n")
	localip = "[+]\nLocal Device"

try:
	import networkmap
	net_map = True
except:
	print "Networkx is needed for visual mapping"
	net_map = False

def rqp(ip):
	try:
		if stop:
			sys.exit()
		ipa = " " + ip + " - " + socket.gethostbyaddr(ip)[0]
		globals()["network"] += ipa[:45]+"\n"
		if net_map:
			ips.append(ip)
			networkmap.rtcheck(ip)
	except Exception as e:
		pass

def netscan((sx1,mx1),(sx2,mx2),(sx3,mx3),(sx4,mx4)):
	"""
	Each pair of numbers is the IP range.
	Example:
	dnsdiscover((8,9),(8,9),(0,40),(0,255))
	Starting IP: 8.8.0.0
	Ending IP:   9.9.40.255
	"""
	for ip in range(sx1,mx1):
		for ipp in range(sx2,mx2):
			for ippp in range(sx3,mx3):
				for ipppp in range(sx4,mx4):
					cip = str(ip)+"."+str(ipp)+"."+str(ippp)+"."+str(ipppp)
					if globals()["stop"]:
						sys.exit()
					t = threading.Thread(target=rqp,args=(cip,))
					t.daemon = True
					try:
						t.start()
					except:
						time.sleep(0.05)
						pass
					time.sleep(0.005)

def config(Interface):
	v["startad"].text = d1
	v["endad"].text = d2

def sconfig(Interface):
	if len(v["startad"].text+v["endad"].text) > 13:
		globals()["d1"] = v["startad"].text
		globals()["d2"] = v["endad"].text

def parse():
	startad = v["startad"]
	endad   = v["endad"]
	if len(startad.text+endad.text) > 13:
		ip1 = startad.text.split(".")
		ip2 = endad.text.split(".")
		syntax = [
			(int(ip1[0]),int(ip2[0])+1),
			(int(ip1[1]),int(ip2[1])+1),
			(int(ip1[2]),int(ip2[2])+1),
			(int(ip1[3]),int(ip2[3])+1)
			]
		return syntax
	return False

def clean(Interface):
	globals()["network"] = ""

def clearin(Interface):
	v["startad"].text = ""
	v["endad"].text = ""

def uiupdate():
	try:
		time.sleep(1)
		while 1:
			v["output"].text = network
			v["at"].text = str(threading.active_count())
			v["devices"].text = str(len(ips))
			time.sleep(0.05)
	except:
		pass

def visualmap(Interface):
	if len(ips) > 25:
		globals()["network"] += "\nToo many nodes for network visualization\n"
		sys.exit()
	if net_map and len(ips) > 1:
		globals()["router"] = networkmap.router
		try:
			v["Image"].hidden = False
		except:
			pass
		v["close"].hidden = False
		networkmap.maps(ips,router,localip)
		v.add_subview(ui.ImageView(name = "Image"))
		image = v["Image"]
		image.image = ui.Image.named("romap_visual.png")
		v["Image"].height = 218.8
		v["Image"].width = 318.8
		v["Image"].frame = (-90,195,489,341)
	elif net_map:
		try:
			v["Image"].hidden = False
		except:
			pass
		v["close"].hidden = False
		v.add_subview(ui.ImageView(name = "Image"))
		image = v["Image"]
		image.image = ui.Image.named("romap_visual.png")
		v["Image"].height = 218.8
		v["Image"].width = 318.8
		v["Image"].frame = (-90,195,489,341)

def threadkill(Interface):
	globals()["stop"] = True
	time.sleep(1)
	globals()["stop"] = False

def show_settings(Interface):
	v["settings_page"].hidden = False
	v["back"].hidden = False

def close_settings(Interface):
	v["settings_page"].hidden = True
	v["back"].hidden = True

def closemap(Interface):
	v["Image"].hidden = True
	v["close"].hidden = True

def net(Interface):
	globals()["ips"] = []
	go = parse()
	if go:
		if go[0][0]<go[0][1] and go[1][0]<go[1][1] and go[2][0]<go[2][1] and go[3][0]<go[3][1]:
			ips = []
			ctime = str(timedelta(seconds = time.time())).split(", ")[1][:11]
			globals()["network"] += "\n %s\n  %s\n %s\n" %("="*(len(ctime)+2),ctime,"="*(len(ctime)+2))
			
			t = threading.Thread(target=netscan, args=(eval(str(go).replace("[","").replace("]",""))),)
			t.daemon = True
			t.start()
		else:
			globals()["network"] += "\n Invalid IP Range\n"
	else:
		globals()["network"] += "\n No Address Range\n"

v = ui.load_view()
v["settings_page"].hidden = True
v["back"].hidden = True
v["close"].hidden = True
v.present(title_bar_color="#222222")

b = threading.Thread(target=uiupdate)
b.start()
