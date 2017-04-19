import networkx as nx
from main_f import srr
from main_f import delete_edge
import community
from main_f import  group



def gen_group_net(g,new_g,start_g):
    for node in g.nodes(data=True):
        if new_g.has_node(node[1]["group"]):
            new_g.node[node[1]["group"]]["ini"]+=node[1]["in"]
            new_g.node[node[1]["group"]]["out"] += node[1]["out"]
            new_g.node[node[1]["group"]]["num"] += node[1]["num"]
            new_g.node[node[1]["group"]]["weight"] += node[1]["weight"]

        else:
            new_g.add_node(node[1]["group"],ini=node[1]["in"],out=node[1]["out"],num=node[1]["num"],
                           weight=node[1]["weight"],label=node[1]["group"])
    for edge in start_g.edges(data=True):
       # print(g.node[start_g.node[edge[1]]["label"]])
        node1=g.node[start_g.node[edge[0]]["label"]]["group"]
        node2=g.node[start_g.node[edge[1]]["label"]]["group"]
        if new_g.has_edge(node1,node2):
            new_g[node1][node2]["weight"]+=edge[2]["weight"]
        else:
            new_g.add_edge(node1, node2, weight=edge[2]["weight"])
def gen_rcc_time():
    global START,STEP
    for i in range(1,20):
        g=nx.read_gexf("data\\test"+str(START)+".gexf")
        delete_edge(g)
        srr(g)

        print()
        '''srr(g)
        new=nx.DiGraph()
        gen_group_net(g,new)
        '''
        START-=STEP
        nx.write_gexf(new_g, "data\\re_rcc"+str(START)+".gexf")
def gen_rcc_net():
    sub_g = nx.read_gexf("data\\test.gexf")
    new_g = nx.DiGraph()
    delete_edge(sub_g)
    srr(sub_g)

    temp=nx.read_gexf("data\\test.gexf")
    gen_group_net(sub_g,new_g,temp)
    nx.write_gexf(new_g,"data\\rcc_text.gexf")
#gen_rcc_net()
def gen_main_rcc():
    group=nx.read_gexf("data\\rcc_group.gexf")

    for node in group.nodes(data=True):
        if sub_g.has_node(node[1]["label"]):
            if node[1]["group"]!="C":
                print(node[1]["group"])
                sub_g.remove_node(node[1]["label"])
    nx.write_gexf(sub_g,"data\\main_rcc.gexf")

def community():
    sub_g = nx.read_gexf("data\\test.gexf")
    new_g=sub_g.to_undirected()
    part=community.best_partition(new_g)
    mod=community.modularity(part,new_g)
    for item in part:
        sub_g.node[item]["group"]=group[part[item]]

    nx.write_gexf(sub_g,"data\\community_detect_test.gexf")
    print(mod)



sub_g=nx.read_gexf("data\\comm_dect_rcc.gexf")
for edge in sub_g.edges(data=True):
    edge[2]["out_ratio"]=edge[2]["weight"]/sub_g.node[edge[0]]["weight"]
    edge[2]["in_ratio"]= edge[2]["weight"] / sub_g.node[edge[1]]["weight"]

nx.write_gexf(sub_g,"data\\com_dect_in_and_out.gexf")












