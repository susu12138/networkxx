import  json
import os
import networkx as nx
import gc
dir_dict={"PhysRevA":"PRA",
          "PhysRevB":"PRB",
          "PhysRevD":"PRD",
          "PhysRevC":"PRC",
          "PhysRevLett":"PRL",
          "PhysRevE":"PRE",
          "PhysRevApplied":"PRAPPLIED",
          "PhysRevX":"PRX"
}
dir_data="D:\\data\\data\\aps-dataset-metadata-2015"
dir_file="D:\\data\\data\\aps-dataset-citations-2015.csv"


DICT=["PRA","PRB","PRC","PRD","PRE","PRI","PRL","PRX","PRAPPLIED"]
group=["A","B","C","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]



dict_A={}
dict_B={}
dict_C={}
dict_D={}
dict_E={}
dict_I={}
dict_X={}
dict_L={}
dict_APP={}
dict_z=[dict_A,dict_B,dict_C,dict_D,dict_E,dict_I,dict_L,dict_APP]
dict_sub_name={}

def get_file_json(str="10.1103/PhysRevA.89.012102"):


    paper=str
    journal=paper.split("/")[1]
    temp=paper.split("/")
    paper=temp[1]
    journal=journal.split(".")
    if journal[0] in dir_dict:
        file_path=os.path.join(dir_data,dir_dict[journal[0]],journal[1],paper+".json")
    else:
        raise KeyError
    #print(file_path)
    try:
        f=open(file_path,encoding="utf8")
    except FileNotFoundError as err:
        #print("in get_file_json file not find")
        raise  FileNotFoundError
    data=json.load(f)
    f.close()
    return data



#generate indree and outgree
def gen_in_out(g,item):
    ini=0
    for i in g.predecessors(item):
        ini+=g[i][item]["weight"]
        print(g[i][item])

    print("...............")
    out=0
    for i in g.successors(item):
        out+=g[item][i]["weight"]
        print(g[item][i])

    print(g.node[item]["weight"])
    #print(str(ini)+"  "+str(out))
    g.node[item]["out"]=out/g.node[item]["weight"]
    g.node[item]["in"]=ini/g.node[item]["weight"]
    if g.has_edge(item,item):
        g.node[item]["self"]=g[item][item]["weight"]/g.node[item]["weight"]
    print(str(g.node[item]["out"])+" "+str(g.node[item]["in"]))


#generate avg_author and indegree
def scan_avgau_and_in_out(g):
    for node in g.nodes():
        g.node[node]["avg_author"] = g.node[node]["sum_author"] / g.node[node]["weight"]
        gen_in_out(g,node)


def insert_sub_dict(data,dict_l):
    if "tocSection" in data.keys():
        if data["tocSection"]["label"] in dict_l.keys():
            dict_l[data["tocSection"]["label"]]+=1
        else:
            dict_l[data["tocSection"]["label"]]=1


def select_insert(data):
    if data["journal"]["id"]==DICT[0]:
        insert_sub_dict(data,dict_A)
    elif data["journal"]["id"]==DICT[1]:
        insert_sub_dict(data, dict_B)
    elif data["journal"]["id"] == DICT[2]:
        insert_sub_dict(data, dict_C)
    elif data["journal"]["id"] == DICT[3]:
        insert_sub_dict(data, dict_D)
    elif data["journal"]["id"] == DICT[4]:
        insert_sub_dict(data, dict_E)
    elif data["journal"]["id"] == DICT[5]:
        insert_sub_dict(data, dict_I)
    elif data["journal"]["id"] == DICT[6]:
        insert_sub_dict(data, dict_L)
    elif data["journal"]["id"] == DICT[7]:
        insert_sub_dict(data, dict_X)
    elif data["journal"]["id"] == DICT[8]:
        insert_sub_dict(data, dict_APP)

def Captitaliza(s):
    new=""
    for i in range(0,len(s)):
        if i ==0:
            new+=s[i].upper()
        elif s[i-1]==" ":
            new+=s[i].upper()
        else:
            new+=s[i]
    return new

def insert_network(Digraph,data1,data2):
    if "tocSection"  in data1:
        l1 = data1["tocSection"]["label"]
    else:
        return 1
    if "tocSection"  in data2:
        l2 = data2["tocSection"]["label"]
    else:
        return 1
    l1=l1.upper()
    l2=l2.upper()

    if Digraph.has_node(l1):
        Digraph.node[l1]["weight"]+=1
        Digraph.node[l1]["sum_author"]+=len(data1["authors"])

    else:
        Digraph.add_node(l1,weight=1,num=1)
        Digraph.node[l1]["journal"] = data1["journal"]["id"]
        Digraph.node[l1]["sum_author"]=len(data1["authors"])
    if Digraph.has_node(l2):
        Digraph.node[l2]["weight"]+=1
        Digraph.node[l2]["sum_author"]+=len(data2["authors"])
    else:
        Digraph.add_node(l2,weight=1,num=1)
        Digraph.node[l2]["journal"] = data2["journal"]["id"]
        Digraph.node[l2]["sum_author"] = len(data2["authors"])
    if Digraph.has_edge(l1.upper(),l2):
        Digraph[l1][l2]["weight"]+=1
    else:
        Digraph.add_edge(l1,l2,weight=1)

    return 0


#divide groupe srr

def uniform_sub(data1,data2):
    if "tocSection"  in data1:
        pass
    elif "classificationSchemes" in data1:
        data1["tocSection"]["label"]=data1["classificationSchemes"]["label"]
    else:
        pass
    if "tocSection"  in data2:
        pass
    elif "classificationSchemes" in data2:
        data2["tocSection"]["label"] = data2["classificationSchemes"]["label"]
    else:
        pass

def srr(g):
    i=0
    for temp in nx.strongly_connected_component_subgraphs(g):
        i+=1
        print("group"+str(i))
        for node in temp.nodes():
            g.node[node]["group"]=group[i]


def delete_edge(g,cut=5):
    for edge in g.edges(data=True):
        if edge[2]["weight"]<cut:
            g.remove_edge(edge[0],edge[1])
            print(edge[2]["weight"])
