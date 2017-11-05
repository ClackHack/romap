import networkx as nx
import matplotlib.pyplot as plt
import random, socket

socket.setdefaulttimeout(2)
router = "[*]\nRouter"

def rtcheck(ip):
	if ip.endswith(".1") or ip.endswith(".254"):
		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		try:
			s.connect((ip,80))
			s.close()
			globals()["router"] = "[*]\n"+ip
		except:
			pass

def draw_graph(graph, labels=None, graph_layout="shell",
node_size=1400, node_color="red", node_alpha=0.65, node_text_size=8,
edge_color="red", edge_alpha=0.8, edge_tickness=0.5, edge_text_pos=5.3, text_font="sans-serif"):
	
	fig, ax = plt.subplots()
	ax.axis("off")
	plt.title("Romap - Static Networkx Map")
	
	G = nx.cycle_graph(" ")
	for edge in graph:
		G.add_edge(edge[0], edge[1])
	if graph_layout == "spring":
		graph_pos=nx.spring_layout(G)
	elif graph_layout == "spectral":
		graph_pos=nx.spectral_layout(G)
	elif graph_layout == "random":
		graph_pos=nx.random_layout(G)
	else:
		graph_pos=nx.shell_layout(G)
	nx.draw_networkx_nodes(G,graph_pos,node_size=node_size, alpha=node_alpha, node_color=node_color)
	nx.draw_networkx_edges(G,graph_pos,width=edge_tickness, alpha=edge_alpha,edge_color=edge_color)
	
	nx.draw_networkx_labels(G, graph_pos,font_size=node_text_size, font_family=text_font)

	edge_labels = dict(zip(graph, labels))
	nx.draw_networkx_edge_labels(G, graph_pos, edge_labels=edge_labels, label_pos=edge_text_pos)
	
	plt.savefig("romap_visual.png")

def genmap(nodes,router,me):
	pub = False
	if not nodes[0].startswith("192.168."):
		pub = True
	elif not pub and nodes[0].startswith("10."):
		pub = True
	elif not pub and nodes[0].startswith("172.16."):
		pub = True
	map = []
	if pub:
		map.append((router,me))
		map.append((router,"[!]\nISP"))
		router = "[!]\nISP"
	for _ in nodes:
		map.append((router,_))
		if random.choice([0,0,0,1]) == 0:
			if not pub:
				map.append((me,_))
		if random.choice([0,0,0,1]) == 1:
			if not pub:
				map.append((_,random.choice(map)[1]))
	return map

def maps(ips,router,local):
	graph = genmap(ips,router,local)
	label = eval("["+"'',"*(len(ips)-1)+"'']")
	draw_graph(graph, graph_layout="shell", labels=label)
