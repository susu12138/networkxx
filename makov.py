import networkx as nx
import numpy as np

dict={"B":0,
"g":1,
"f":2,
"h":3,
"e":4,
"d":5,
"C":6,
"A":7,
"j":8,
"i":9}
sub_g=nx.read_gexf("data\\comm_dect_rcc.gexf")
num=sub_g.number_of_nodes()
#print("num "+str(num))

_mat=np.mat(np.zeros((num,num)))
#print(_mat.size)
for edge in sub_g.edges(data=True):
    _mat[dict[edge[0]],dict[edge[1]]]=edge[2]["weight"]



n_mat=_mat.transpose()
#x,y=np.linalg.eig(n_mat)

print(n_mat)
print("\n")
temp=n_mat.sum(axis=1)

for i in range(0,n_mat.shape[0]):
    for j in range(0,n_mat.shape[1]):
        n_mat[i,j]=n_mat[i,j]/temp[i]


x,y =np.linalg.eig(n_mat)
print(y)
print(x)




