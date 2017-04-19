import networkx as nx
import os
import json
import csv
from main_f import get_file_json
from main_f import insert_network
from main_f import scan_avgau_and_in_out
from main_f import select_insert
from main_f import srr
from main_f import  dir_file
sub_g = nx.DiGraph()


def get_attr(graph):
    for node in graph.nodes():
        print(node+" "+str(graph.node[node]["weight"])+"\n")

    print("..............")
def scan_csv_get_sub(file_path,g):
    with open(file_path) as csvfile:
        file=csv.reader(csvfile)

        i=1
        line_pre=""
        for line in file:
            i+=1
            if i<START:
                continue
            elif i<START+STEP:
                #print(i)
                try:
                    data1=get_file_json(line[0])
                    data2=get_file_json(line[1])
                except KeyError as err:
                    #print("scan_file filename key error,pass")
                    continue
                except FileNotFoundError as err:
                    #print("scan file file not find haha")
                    continue
                #print(data1["date"]+"  "+data2["date"])
                insert_network(g,data1,data2)
                if line_pre==line[1]:
                    continue
                elif "tocSection" in data2 and g.has_node(data2["tocSection"]["label"]):
                    g.node[data2["tocSection"]["label"]]["num"]+=1
                line_pre=line[1]
        print("-------------------")

START=6900000
STEP=38000
def gen_net():
    for i in range(1,20):
        global START,STEP
        sub_g = nx.DiGraph()
        scan_csv_get_sub(dir_file,sub_g)
        scan_avgau_and_in_out(sub_g)
#srr(sub_g)
        nx.write_gexf(sub_g,"data\\test"+str(START)+".gexf")
        START=START-STEP

scan_csv_get_sub(dir_file, sub_g)
scan_avgau_and_in_out(sub_g)
nx.write_gexf(sub_g, "data\\test.gexf")



#gen_net()










