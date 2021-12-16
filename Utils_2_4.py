import pandas as pd
import networkx as nx
import pickle 
import random 
import numpy as np
from heapq import heapify, heappush, heappop
from utils import new_graph,dijkstra,traceback,create_path

#given a path and a graph find the the edge with the smallest weight
def find_min(l,dG):
    mi=[]
    for edge in l:
        diz=dG.get_edge_data(*edge)
        cost=diz["weight"]
        mi.append((edge,cost))
    mi=sorted(mi,key= lambda x : x[1])
    return mi[0][0]    

#it creates a new directed weighted graph where a edge weight corrisponds to the sum all the edges weight #that happened in our interval of time
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

#it computes the number of edges we need to remove( considering their weights)
def Min_cut(G,user1,user2,startingTime,endTime,mapping):
    G=new_graph_SumWeights(G,startingTime,endTime)
    cost=0
    edges=[]
    path=True
    while path:
        pred=dijkstra(user1,user2,G,startingTime,endTime,mapping)
        if pred[user2]==-1:
            return cost,edges
        l=traceback(pred,user2,user1)
        l=create_path(l)
        edge=find_min(l,G)
        diz=G.get_edge_data(*edge)
        cost+=diz["weight"]
        edges.append(edge)
        G.remove_edge(*edge)
    return cost,edges


#it finds two users that are not in the same interval of time
def findUser(t1,t2,s1,s2,G):
    g1=new_graph(G,startingTime,endTime)
    g2=new_graph(G,startingTime,endTime)
    set1=set(g1.nodes())
    set2=set(g2.nodes())
    oneS=set1-set2
    twoS=set2-set1
    user1=oneS.pop()
    user2=twoS.pop()
    return user1,user2