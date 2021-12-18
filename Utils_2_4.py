import pandas as pd
import networkx as nx
import pickle 
import random 
import matplotlib.pyplot as plt
import numpy as np
from heapq import heapify, heappush, heappop
from utils_2_3 import new_graph,dijkstra,traceback,create_path

#given a path and a graph it finds  the edge with the smallest weight
def find_min(l,dG):
    mi=[]
    for edge in l:
        diz=dG.get_edge_data(*edge)
        cost=diz["weight"]
        mi.append((edge,cost))
    mi=sorted(mi,key= lambda x : x[1])
    return mi[0][0]    

#it creates a new directed weighted graph where a edge  weight corrisponds to the sum of all the edges' weights of interactions happened between those two nodes
def new_graph_SumWeights(H,startingTime,endTime):
    G = nx.DiGraph()
    edges=H.edges()
    for start_node,end_node in edges:
        diz=H.get_edge_data(start_node,end_node)
        l=sorted(diz.items(),key= lambda x : x[1]["weight"])
        t_weight=0
        for el in l:
            if startingTime<=el[0] and endTime>=el[0]:
                t_weight+=el[1]["weight"]
        if t_weight!=0:
            G.add_edge(start_node, end_node, weight=t_weight)
    return G

#it computes the list of edges we need to remove( considering their weights)
def Min_cut(G,user1,user2,startingTime,endTime,mapping):
    G=new_graph_SumWeights(G,startingTime,endTime)
    cost=0
    edges=[]
    path=True
    while path:
        print("looking for a new path...")
        pred=dijkstra(user1,user2,G,mapping)
        #if user1 and user2 are not connected then pred[user2]==-1
        if pred[user2]==-1:
            print("the minimum number of links (considering their weight) is ",len(edges))
            return cost,edges
        seq=traceback(pred,user2,user1)
        l=create_path(seq)
        print("The path is :",l)
        edge=find_min(l,G)
        diz=G.get_edge_data(*edge)
        cost+=diz["weight"]
        edges.append(edge)
        visualize_minCut(G,edges,seq)
        G.remove_edge(*edge)
    
    return cost,edges


#it finds two users that are not in the same interval of time
def findUser(t1,t2,s1,s2,G):
    g1=new_graph(G,t1,t2)
    g2=new_graph(G,s1,s2)
    set1=set(g1.nodes())
    set2=set(g2.nodes())
    oneS=set1-set2
    twoS=set2-set1
    user1=oneS.pop()
    user2=twoS.pop()
    return user1,user2

#it visualize the path that links the nodes
def visualize_minCut(H,l,nodes):
    print("Here, the path that links {} and {}".format(nodes[0],nodes[-1]))
    print()
    print("The starting and the end node are filled with red")
    print("The link that will be removed,it is evidenced by a red edge".format(nodes[0],nodes[-1]))
    plt.figure(num=None, figsize=(15, 15),dpi=60)
    H = H.subgraph(nodes)
    pos = nx.spring_layout(H)
    edge_colors = ['red' if e in l else "black"   for e in H.edges()] 

    path=[]
    cont=0
    for u in H.nodes:
        if u==nodes[0] or u==nodes[-1]:
            path.append("red")
        else:
            path.append("blue")
    
    nx.draw(H, pos,with_labels=True,edge_color=edge_colors, connectionstyle='arc3, rad = 0.1',arrowsize=30,node_size=2100)
    nx.draw_networkx_nodes(H, pos,node_color=path)
    edge_labels = nx.get_edge_attributes(H,'weight')
    
    

    diz={}
    for u,v in edge_labels:
        diz[(u,v)]=edge_labels[(u,v)]
        
    nx.draw_networkx_edges(H, pos, width=1,style="dotted",edge_color="white")
    nx.draw_networkx_edge_labels(H, pos, edge_labels = diz,label_pos=0.2,font_size=20)
    
    plt.show()
