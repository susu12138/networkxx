import csv
import networkx as nx
import gc
from collections import OrderedDict
from main_f import get_file_json
from main_f import insert_network
from main_f import scan_avgau_and_in_out
from main_f import select_insert
from main_f import srr
from main_f import uniform_sub
from main_f import  dir_file

START=5000000
total=6980000
STEP=38000
year={}
#update


class gen_net:
    def __init(self):
        pass

    def scan_csv_get_sub(file_path,g):
        with open(file_path) as csvfile:
            file=csv.reader(csvfile)
            i=1
            line_pre=""
            year_pre=0
            for line in file:
                i+=1
                if i<START:
                    continue
                else:
                    if i%2000==0:
                        print((i-START)/(total-START))
                    if i%50000==0:
                        gc.collect()

                    try:
                        data1=get_file_json(line[0])
                        data2=get_file_json(line[1])
                        #uniform_sub(data1,data2)
                        data1["tocSection"]["label"]+=data1["date"][:4]
                        data2["tocSection"]["label"]+=data2["date"][:4]


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
                    if int(data2["date"][:4]) in year:
                        year[int(data2["date"][:4])] += 1
                    else:
                        year[int(data2["date"][:4])] = 1
                    line_pre=line[1]
            print("-------------------")
    #gennerate real timeline based network
    def gen_timeline_net(self):
        s=nx.DiGraph()
        scan_csv_get_sub(dir_file,s)
        scan_avgau_and_in_out(s)
        nx.write_gexf(s,"data\\timeline_test_l.gexf")
        for item in year:
            print(str(item)+" "+str(year[item]))


    def merge_node(new_g,g,node1):
        node_name=node1[:6]+node1[-4:]
        if node_name not in new_g:
            new_g.add_node(node_name,num=g.node[node1]["num"],sum_author=g.node[node1]["sum_author"],journal=g.node[node1]["journal"])
            for node in g.predecessors(node1):
                if g.node[node]["isMerged"]==True:
                    continue
                node_name2=node[:6]+node[-4:]
                if new_g.has_edge(node_name2, node_name):
                    new_g[node_name2][node_name]["weight"] += g[node][node1]["weight"]
                else:
                    new_g.add_edge(node_name2, node_name, weight=g[node][node1]["weight"])

            for node in g.successors(node1):
                if g.node[node]["isMerged"]==True:
                    continue
                node_name2=node[:6]+node[-4:]
                if new_g.has_edge(node_name, node_name2):
                    new_g[node_name][node_name2]["weight"] += g[node1][node]["weight"]
                else:
                    new_g.add_edge(node_name, node_name2, weight=g[node1][node]["weight"])
        else:
            if "num" not in new_g.node[node_name]:
                print(new_g.node[node_name])
                new_g.node[node_name]["num"]=g.node[node1]["num"]
                new_g.node[node_name]["sum_author"]=g.node[node1]["sum_author"]
                new_g.node[node_name]["journal"] = g.node[node1]["journal"]
            else:
                new_g.node[node_name]["num"] += g.node[node1]["num"]
                new_g.node[node_name]["sum_author"] += g.node[node1]["sum_author"]
            for node in g.predecessors(node1):
                if g.node[node]["isMerged"]==True:
                    continue
                node_name2=node[:6]+node[-4:]
                if new_g.has_edge(node_name2, node_name):
                    new_g[node_name2][node_name]["weight"] += g[node][node1]["weight"]
                else:
                    new_g.add_edge(node_name2, node_name, weight=g[node][node1]["weight"])

            for node in g.successors(node1):
                if g.node[node]["isMerged"]==True:
                    continue
                node_name2=node[:6]+node[-4:]
                if new_g.has_edge(node_name, node_name2):
                    new_g[node_name][node_name2]["weight"] += g[node1][node]["weight"]
                else:
                    new_g.add_edge(node_name, node_name2, weight=g[node1][node]["weight"])
        print("delete"+node1)




    #call merge_node function
    def merge_multiName_net(self):

        g = nx.read_gexf("data\\timeline_test.gexf")

        new_g=nx.DiGraph()
        for node in g.nodes():
            g.node[node]["isMerged"]=False
        for node in g.nodes():
            if g.node[node]["isMerged"] == True:
                continue
            self.merge_node(new_g,g,node)
            g.node[node]["isMerged"] = True

        nx.write_gexf(new_g,"data\\timeline_new_g.gexf")
    def equal_zero(self,a,e=0.000001):
        if a<e and a>-e:
            return True
        else:
            return False

    #generate one node attribute
    def gen_avg_cited_year(g,node):
        weighted_sum=0.0
        sum=0.0
        year=int(node[-4:])
        print(year)
        for i in g.successors(node):
            year1=int(i[-4:])
            sum+=g[node][i]["weight"]
            weighted_sum+=g[node][i]["weight"]*(year-year1)

        g.node[node]["out"]=sum
        if self.equal_zero(sum):
            g.node[node]["avg_year_out"] = 0
        else:
            g.node[node]["avg_year_out"] = weighted_sum / sum



        weighted_sum = 0.0
        sum = 0.0
        for i in g.predecessors(node):
            year1=int(i[-4:])
            sum+=g[i][node]["weight"]
            weighted_sum+=g[i][node]["weight"]*(year1-year)
        g.node[node]["in"]=sum
        if self.equal_zero(sum):
            g.node[node]["avg_year_in"] = 0
        else:
            g.node[node]["avg_year_in"] = weighted_sum / sum

    def merge_node_without_year(self,new_g, g, node1):
        node_name = node1[:6]
        if node_name not in new_g:
            new_g.add_node(node_name, num=g.node[node1]["num"], sum_author=g.node[node1]["sum_author"],
                           journal=g.node[node1]["journal"])
            for node in g.predecessors(node1):
                if g.node[node]["isMerged"] == True:
                    continue
                node_name2 = node[:6]
                if new_g.has_edge(node_name2, node_name):
                    new_g[node_name2][node_name]["weight"] += g[node][node1]["weight"]
                else:
                    new_g.add_edge(node_name2, node_name, weight=g[node][node1]["weight"])

            for node in g.successors(node1):
                if g.node[node]["isMerged"] == True:
                    continue
                node_name2 = node[:6]
                if new_g.has_edge(node_name, node_name2):
                    new_g[node_name][node_name2]["weight"] += g[node1][node]["weight"]
                else:
                    new_g.add_edge(node_name, node_name2, weight=g[node1][node]["weight"])
        else:
            if "num" not in new_g.node[node_name]:
                print(new_g.node[node_name])
                new_g.node[node_name]["num"] = g.node[node1]["num"]
                new_g.node[node_name]["sum_author"] = g.node[node1]["sum_author"]
                new_g.node[node_name]["journal"] = g.node[node1]["journal"]
            else:
                new_g.node[node_name]["num"] += g.node[node1]["num"]
                new_g.node[node_name]["sum_author"] += g.node[node1]["sum_author"]
            for node in g.predecessors(node1):
                if g.node[node]["isMerged"] == True:
                    continue
                node_name2 = node[:6]
                if new_g.has_edge(node_name2, node_name):
                    new_g[node_name2][node_name]["weight"] += g[node][node1]["weight"]
                else:
                    new_g.add_edge(node_name2, node_name, weight=g[node][node1]["weight"])

            for node in g.successors(node1):
                if g.node[node]["isMerged"] == True:
                    continue
                node_name2 = node[:6]
                if new_g.has_edge(node_name, node_name2):
                    new_g[node_name][node_name2]["weight"] += g[node1][node]["weight"]
                else:
                    new_g.add_edge(node_name, node_name2, weight=g[node1][node]["weight"])
        print("delete" + node1)
    def merge_multiName_net_without_year(self,g):
        new_g=nx.DiGraph()
        for node in g.nodes():
            g.node[node]["isMerged"]=False
        for node in g.nodes():
            if g.node[node]["isMerged"] == True:
                continue
            self.merge_node_without_year(new_g,g,node)
            g.node[node]["isMerged"] = True
        return new_g

    #add a new attribute to sub_net_year
    def gen_avg_cited_net(self):
        g=nx.read_gexf("data\\timeline_new_g.gexf")
        for node in g:
            self.gen_avg_cited_year(g,node)

        nx.write_gexf(g,"data\\timeline_new_g.gexf")

    def gen_group_net(g,new_g,start_g):
        for node in g.nodes(data=True):
            if new_g.has_node(node[1]["group"]):
                new_g.node[node[1]["group"]]["in"]+=node[1]["in"]
                new_g.node[node[1]["group"]]["out"] += node[1]["out"]
                new_g.node[node[1]["group"]]["num"] += node[1]["num"]
                new_g.node[node[1]["group"]]["sum_author"] += node[1]["sum_author"]

            else:
                new_g.add_node(node[1]["group"], in_=node[1]["in"],out=node[1]["out"],num=node[1]["num"],
                               weight=node[1]["weight"],label=node[1]["group"])
        for edge in start_g.edges(data=True):
           # print(g.node[start_g.node[edge[1]]["label"]])
            node1=g.node[start_g.node[edge[0]]["label"]]["group"]
            node2=g.node[start_g.node[edge[1]]["label"]]["group"]
            if new_g.has_edge(node1,node2):
                new_g[node1][node2]["weight"]+=edge[2]["weight"]
            else:
                new_g.add_edge(node1, node2, weight=edge[2]["weight"])

    def gen_new_net(self):
        self.merge_multiName_net()
        self.gen_avg_cited_net()
    def changeToNum(self,strl):
        sum=0
        a = ord('a')
        z=ord('z')
        A=ord('A')
        Z=ord('Z')
        for i in strl:
            temp=ord(i)
            if temp>=a and temp<=z:
                temp=temp-ord('a')
            elif temp>=A and temp<=Z:
                temp=temp-ord('A')
            sum=sum*100+temp
        return sum
    def changeToStr(self,num):
        strl=""
        a = ord('a')
        num=int(num)
        while(num):
            temp=(num % 100)+a
            strl+=chr(temp)
            num=(int)(num/100)
        return strl[::-1]
    def test_hash(self):
        str="hello"
        temp=self.changeToNum(str)
        print(temp)
        print(self.changeToStr(temp))

    def relabel_net(self,g):
        mapping={k:self.changeToNum(k) for k in g.nodes()}
        new_g=nx.relabel_nodes(g,mapping)
        return new_g
    def relabel_net_re(self,g):
        mapping={k:self.changeToStr(k) for k in g.nodes()}
        new_g=nx.relabel_nodes(g,mapping)
        return new_g
    def gen_net_without_year(self):
        g = nx.read_gexf("data\\timeline_new_g_l.gexf")
        new_g=self.merge_multiName_net_without_year(g)
        g=self.relabel_net(new_g)
        nx.write_gexf(g,"data\\timeline_new_g_l_relabel.gexf")



class cal_imapct_factor:
    def __init__(self):
        self.g=nx.read_gexf("data\\timeline_new_g.gexf")

    def gen_sub_dict(self):
        for node in self.g.nodes():
            sub=node[:-4]
            if sub in self.dictl:
                continue
            else:
                self.dictl[sub]=1

    def cal_oneNode_impact(self,node):
        if node not in self.g.nodes():
            print("node not exits")
            return
        year=int(node[-4:])
        year1=year-1
        year2=year-2
        node1=node[:-4]+str(year1)
        node2=node[:-4]+str(year2)
        if node1 not in self.g.nodes():
            print("year1 not exist")
            return
        if node2 not in self.g.nodes():
            print("year2 not exist")
            return
        sum1=0
        sum2=2
        for item in self.g.nodes():
            y=int(item[-4:])
            if y!=year:
                continue
            else:
                if self.g.has_edge(item,node1):
                    sum1+=self.g[item][node1]["weight"]
                if self.g.has_edge(item,node2):
                    sum2+=self.g[item][node2]["weight"]

        self.g.node[node]["impact_factor"]=(sum1+sum2)/(self.g.node[node1]["num"]+self.g.node[node2]["num"])

    def cal_impact_factor(self):
        for node in self.g.nodes():
            self.cal_oneNode_impact(node)
        self.save()

    def save(self):
        nx.write_gexf(self.g,"data\\timeline_new_g_l.gexf")

a=gen_net()
a.gen_net_without_year()

















