import numpy
import deepwalk
import networkx as nx

g=nx.read_gexf("data\\timeline_new_g_l.gexf")

a=deepwalk(g)