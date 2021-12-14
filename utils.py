import pandas as pd
import networkx as nx
import pickle 
import random 
import numpy as np
from heapq import heapify, heappush, heappop

def path(startingNode,endNode,index,H,startingTime,endTime):
    index.insert(0,startingNode)
    index.append(endNode)
    #it creates the new graph
    dG=new_graph(H,startingTime,endTime)
    paths = iter(index)
    final_path=[]
    c=list(zip(paths, paths))
    c=links(c)
    print("the path is ",c)
    for start,end in c:
        print(start)
        if start  not in dG.nodes(): 
            print("{} doesn't interact in the chosen interval of time".format(start))
            return final_path
        if end not in dG.nodes():
            print("{} doesn't interact in the chosen interval of time".format(end))
            return final_path
        pred=dijkstra(start,end,dG,startingTime,endTime)
        #check if 2 nodes are not connected
        if  pred[end]==np.inf:
            break
        path=traceback(pred,end,start)
        if final_path:
            final_path.extend(path[1:])
        else :
             final_path.extend(path)
    return final_path

#it adds the tuples that created the list of edges that we neet to build the path between the nodes
def links(index):
    full_links=[]
    l=len(index)
    for i in range(l-1):
        full_links.append(index[i])
        v=index[i][1]
        v2=index[i+1][0]
        full_links.append((v,v2))
    full_links.append(index[l-1])
    return full_links
        
        
#it renames the nodes and return the mapping between nodes and integers
def first(G_loaded):
    dG,mapping=maps(G_loaded)
    index=random_path(8,mapping)
    return dG,index

#it returns the random path
def random_path(n,mapping):
    random.seed(12)
    l=random.sample(set(mapping.keys()),n-2 )
    index=labels(l,mapping)
    return index

#it maps the nodes with integers from 0
def maps(G):
    mapping = {node:index for index, node in enumerate(G.nodes())}
    H = nx.relabel_nodes(G, mapping)
    return H,mapping

#it renames the random path
def labels(l,mapping):
    l=[mapping[i] for i in l]
    return l

#the dijkstra algorithm
def dijkstra(Starting_vertex,End_vertex,dG,startingTime,endTime):
    N=len(dG.nodes())
    #it creates the min_heap
    min_heap = []
    heapify(min_heap)
    
    Final_distance=0
    dist=np.ones(N)* np.inf
    visited=np.zeros(N, dtype=bool)
    pred=np.ones(N,dtype="int64")*(-1)
    
    #it loads the starting vertex
    heappush(min_heap, (0,Starting_vertex))
    end=False
    dist[Starting_vertex]=0
    
    # for each node i'm looking for the best path from the starting node
    while min_heap and not end:
        element = heappop(min_heap)[1]
        #it creates a set of (u,v) edges
        for start_node,end_node in list(dG.edges(element)):
                
            if not visited[end_node]:
                diz=dG.get_edge_data(start_node,end_node)
                weight=diz["weight"]
                distance=dist[end_node]
                #check if distance is smaller
                if distance> dist[element] + weight:
                    #if we already accessed this node
                    if distance!=np.inf:
                        min_heap.remove((distance,end_node))
                        dist[end_node]=dist[element] + weight
                        heappush(min_heap, (dist[end_node],end_node))
                        heapify(min_heap)
                    else:
                        dist[end_node]=dist[element] + weight
                        heappush(min_heap, (dist[end_node],end_node))

                    #to remember the predecessor to traceback
                    pred[end_node]=element
        visited[element]=True
        
        #I break the loop when i arrive to to the node i'm looking for (Gready algorith)
        if element == End_vertex:
            Final_distance=dist[element]
            end=True
            print("Final_distance between {} and {} ".format(Starting_vertex,End_vertex),Final_distance)
            
    #if during all the path we don't reach the End_vertex means the 2 nodes are not connected
    if not end:
        print("there isn't a path between this 2 values {} and {}".format(Starting_vertex,End_vertex))
        return pred
    return pred

#it computes the path from the starting node to the endNode
def traceback(pred,target,start):
    res=[]
    res.insert(0,target)
    while pred[target]!=start:
        target=pred[target]
        res.insert(0,target)
    res.insert(0,start)
    return res

#it computes all the paths using the nx.all_simple_paths method to check the weight
#we find the smaller one weight to go from the starting node to the end node
def check(dG,starting,end,startingTime,endTime,cutoff):
    dG=new_graph(dG,startingTime,endTime)
    paths = nx.all_simple_paths(dG, starting, end,cutoff)
    old=100000
    tot_weight=0
    for path in map(nx.utils.pairwise, paths):
        paths=list(path)
        for start, end in paths:
            diz=dG.get_edge_data(start,end)
            tot_weight+=diz["weight"]
        if tot_weight<old:
            old=tot_weight
            print("path is {}, total weight is {} ".format(paths,tot_weight))
        tot_weight=0
        
#it computes the new graph with only the links in a time interval  that have the smaller weight     
def new_graph(H,startingTime,endTime):
    G = nx.DiGraph()
    edges=H.edges()
    for start_node,end_node in edges:
        diz=H.get_edge_data(start_node,end_node)
        #it creates a new graph only with interactions that happened in the desired interval
        l=sorted(diz.items(),key= lambda x : x[1]["weight"])
        for el in l:
            if startingTime<=el[0] and endTime>=el[0]:
                G.add_edge(start_node, end_node, weight=el[1]["weight"])
                break
    return G