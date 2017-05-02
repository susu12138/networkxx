import numpy as np
import matplotlib.pyplot as plt

import networkx as nx
class ReadVec:
    def __init__(self):
        self.read_v()
        self.show()
    def read_v(self):
        dic = {}
        with open("data/node2vec.emb","r") as f:
            i=1
            for line in f:
                if i ==1:
                    i+=1
                    continue
                v=line.split()
                l=len(v)
                temp_v=np.zeros(l-1)
                for i in range(1,l):
                    temp_v[i-1]=v[i]
                dic[v[0]]=temp_v
        return dic
    def show(self):
        self.new_dic={}
        dic=self.read_v()
        for line in dic:
            self.new_dic[self.changeToStr(int(line)).upper()]=dic[line]

        self.com_cosine_matrix()
        print(self.mapping)
        #print(self.cos)
        print(self.max)
        self.year_interve=self.max/14


    def changeToStr(self, num):
        strl = ""
        a = ord('a')
        num = int(num)
        i=1
        while (i<=6):
            temp = (num % 100)
            if temp<=27:
                temp=temp+a
            else:
                print("haha"+str(temp))
            strl += chr(temp)
            num = (int)(num / 100)
            i+=1
        return strl[::-1]
    def com_cosine_matrix(self):
        l=len(self.new_dic)
        self.mapping={}
        self.cos=np.zeros((l,l))
        i=0
        for item in self.new_dic:
            self.mapping[item]=i
            i+=1

        max = 0
        for x in self.new_dic:
            for y in self.new_dic:
                i=self.mapping[x]
                j=self.mapping[y]
                self.cos[i,j]=np.sqrt(np.sum(np.square(self.new_dic[x]-self.new_dic[y])))
                if max<self.cos[i,j]:
                    max=self.cos[i,j]
        self.max=max
class Connection:
    def cal_connection_node(self,a,interval):
        g=nx.read_gexf("data/timeline_new_g_l.gexf")
        year=2002
        for node in g:
            index=node[:6].upper()

            t=int(node[6:])
            g.node[node]["array_1"]=np.asscalar(a[index][0])
            g.node[node]["array_2"]=np.asscalar(a[index][1])
            g.node[node]["array_3"]=np.asscalar((t-year)*interval)
        nx.write_gexf(g,"data/timeline_new_g_l_node2vec.gexf")
def c():
    b=ReadVec()
    print(b.new_dic)
    a=Connection()
    interval=b.max/25
    a.cal_connection_node(b.new_dic,interval)

class Conn:
    def __init__(self,path="data/timeline_new_g_l_node2vec.gexf"):
        self.g=nx.read_gexf(path)
        self.path=path
    def relabel(self,strl):
        temp=strl[:6].upper()
        temp+=strl[6:]
        return temp
    def relabel_net(self):
        mapping = {k:self.relabel(k) for k in self.g.nodes()}
        new_g=nx.relabel_nodes(self.g,mapping)
        self.g=new_g
        nx.write_gexf(self.g,self.path)

    def core(self):
        for node in self.g:
            self.g.node[node]["is_cal"]=False
        for node in self.g:
            if self.g.node[node]["is_cal"]:
                continue
            else:
                year=int(node[6:])
                self.g.node[node]["is_cal"]=True
                pre_vec=self.find_forward_node(node)
                bak_vec=self.find_backward_node(node)
                pre_node=node[:6]+str(year-1)
                if self.g.has_node(pre_node):
                    p_vec=self.find_forward_node(pre_node)
                    b_vec=self.find_backward_node(pre_node)
                else:
                    continue
                ans=0
                for i in range(0,3):
                    if p_vec[i] == pre_node or pre_vec[i]==node:
                        continue
                    a = self.g.node[p_vec[i]]["array_1"]-self.g.node[pre_node]["array_1"]
                    b = self.g.node[p_vec[i]]["array_2"] - self.g.node[pre_node]["array_2"]
                    c = self.g.node[p_vec[i]]["array_3"] - self.g.node[pre_node]["array_3"]
                    e = self.g.node[pre_vec[i]]["array_1"] - self.g.node[node]["array_1"]
                    f = self.g.node[pre_vec[i]]["array_2"] - self.g.node[node]["array_2"]
                    g = self.g.node[pre_vec[i]]["array_3"] - self.g.node[node]["array_3"]
                    a=a-e
                    b=b-f
                    c=c-g
                    ans+=(a*a+b*b+c*c)
                    if pre_node==b_vec[i] or node==bak_vec[i]:
                        continue
                    a = self.g.node[pre_node]["array_1"] - self.g.node[b_vec[i]]["array_1"]
                    b = self.g.node[pre_node]["array_2"] - self.g.node[b_vec[i]]["array_2"]
                    c = self.g.node[pre_node]["array_3"] - self.g.node[b_vec[i]]["array_3"]
                    e = self.g.node[node]["array_1"] - self.g.node[bak_vec[i]]["array_1"]
                    f = self.g.node[node]["array_2"] - self.g.node[bak_vec[i]]["array_2"]
                    g = self.g.node[node]["array_3"] - self.g.node[bak_vec[i]]["array_3"]
                    a = a - e
                    b = b - f
                    c = c - g
                    ans += (a * a + b * b + c * c)
                self.g.node[node]["ans"]=ans
                print(node,end=" ")
                print(ans)

        nx.write_gexf(self.g,self.path)

    def display(self,strl):
        year=2002
        y=np.zeros(13)
        for i in range(year,2015):
            node=strl+str(i)
            if self.g.has_node(node):
                try:
                    y[i-year]=self.g.node[node]["ans"]
                except KeyError:
                    continue
            else:
                pass
        x=np.arange(year,2015,1)
        return x,y

    def bat_display(self):
        dic_node={}

        for node in self.g.nodes():
            item=node[:6]
            dic_node[item]=1
        print(dic_node.__len__())
        i=1
        for k in dic_node.keys():
            x,y=self.display(k)
            yield x,y,k



    def find_forward_node(self,node):
        max=[0,-1,-2]
        max_node=[node,node,node]
        for i in self.g.predecessors(node):
            t=i[:6]
            if t==node[:6] or t==max_node[0][:6] or t==max_node[1][:6] or t == max_node[2][:6]:
                continue
            temp=self.g[i][node]["weight"]

            if temp>max[0]:
                max[2]=max[1]
                max[1]=max[0]
                max[0]=temp
                max_node[2]=max_node[1]
                max_node[1]=max_node[0]
                max_node[0]=i
            elif temp>max[1]:
                max[2]=max[1]
                max[1]=temp
                max_node[2]=max_node[1]
                max_node[1]=i
            elif temp>max[2]:
                max[2]=temp
                max_node[2]=i
        return max_node
    def find_backward_node(self,node):
        max = [0, -1, -2]
        max_node = [node, node, node]
        for i in self.g.successors(node):
            if i[:6]==node[:6]:
                continue
            temp = self.g[node][i]["weight"]

            if temp > max[0]:
                max[2] = max[1]
                max[1] = max[0]
                max[0] = temp
                max_node[2] = max_node[1]
                max_node[1] = max_node[0]
                max_node[0] = i
            elif temp > max[1]:
                max[2] = max[1]
                max[1] = temp
                max_node[2] = max_node[1]
                max_node[1] = i
            elif temp > max[2]:
                max[2] = temp
                max_node[2] = i
        return max_node
    def plot_connection(self,strl):

        a=plt.subplot(1,2,1)
        self.plot_vec(a,strl)
        year=int(strl[6:])-1
        new_node=strl[:6]+str(year)
        b=plt.subplot(1,2,2)
        self.plot_vec(b,new_node)
        plt.show()
    def plot_vec(self,plt_a,node):
        bak_node = self.find_backward_node(node)
        pre_node = self.find_forward_node(node)
        for i in range(0, 3):
            x = [self.g.node[bak_node[i]]["array_3"], self.g.node[node]["array_3"]]
            y = [self.g.node[bak_node[i]]["array_2"], self.g.node[node]["array_2"]]
            plt_a.plot(x, y)
            print(x,end="   ")
            print(y,end="\n")

            x = [self.g.node[pre_node[i]]["array_3"], self.g.node[node]["array_3"]]
            x = [self.g.node[pre_node[i]]["array_2"], self.g.node[node]["array_2"]]
            plt_a.plot(x, y)
            print(i)








a=Conn()
b=a.find_forward_node("MAGNET2004")
a.plot_connection("MAGNET2004")
#















