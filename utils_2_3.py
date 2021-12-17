import pandas as pd
import networkx as nx
import pickle 
import random 
import matplotlib.pyplot as plt

import numpy as np
from heapq import heapify, heappush, heappop

def path(startingNode,endNode,index,H,startingTime,endTime,mapping):
    index.insert(0,startingNode)
    index.append(endNode)
    #it creates the new graph
    dG=new_graph(H,startingTime,endTime)
    c=create_path(index)
    final_path=[]
    print("the sequnce of nodes : ")
    print(index)
    for start,end in c:
        if start  not in dG.nodes(): 
            print("the node {} doesn't interact in the chosen interval of time".format(start))
            return final_path
        if end not in dG.nodes():
            print("the node {} doesn't interact in the chosen interval of time".format(end))
            return final_path
        pred=dijkstra(start,end,dG,mapping)
        #check if 2 nodes are not connected
        if  pred[end]==-1:
            break
        path=traceback(pred,end,start)
        if final_path:
            final_path.extend(path[1:])
        else :
             final_path.extend(path)
                
    #it create the path as a list of tuples
    p=create_path(final_path)
    #it invokes the visualization method
    visualizePath(dG,final_path,p)
    return final_path

#it adds the all the tuples that we need to  create the list of edges componing the path 
def links(index):
    full_links=[]
    l=len(index)
    for i in range(l-1):
        full_links.append(index[i])
        v=index[i][1]
        v2=index[i+1][0]
        if v!=v2:
            full_links.append((v,v2))
    full_links.append(index[l-1])
    return full_links
        
        
#it renames the nodes and return the mapping between nodes and integers and the random path
def first(G_loaded):
    dG,mapping=maps(G_loaded)
    index=random_path(8,mapping)
    return dG,index,mapping

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
def dijkstra(Starting_vertex,End_vertex,dG,mapping):
    #it creates the min_heap
    min_heap = []
    heapify(min_heap)
    N=len(mapping)
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
                #check if distance is bigger
                if distance> dist[element] + weight:
                    #if we have already accessed this node
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
            print("the smallest path distance between {} and {} is ".format(Starting_vertex,End_vertex),Final_distance)
            
    #if during all the path we don't reach the End_vertex means the 2 nodes are not connected
    if not end:
        print("there isn't a path between this two values {} and {}".format(Starting_vertex,End_vertex))
        
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


        
#it computes the new graph with only the links in a time interval  that have the smaller weight     
def new_graph(H,startingTime,endTime):
    G = nx.DiGraph()
    edges=H.edges()
    for start_node,end_node in edges:
        diz=H.get_edge_data(start_node,end_node)
        #it creates a new graph only with interactions that happened in the desired interval
        #and it takes the othe the smallest weight
        l=sorted(diz.items(),key= lambda x : x[1]["weight"])
        for el in l:
            if startingTime<=el[0] and endTime>=el[0]:
                G.add_edge(start_node, end_node, weight=el[1]["weight"])
                break
    return G

def create_path(l):
    paths = iter(l)
    c=list(zip(paths, paths))
    if len(l)%2!=0:
        c.append((l[-2],l[-1]))
    c=links(c)
    return c      

#it creates the graph to visualize the path
def visualizePath(dg,nodes,p):
    print("The path that we need to follow is ",p)
    print()
    print("The starting and the end node are filled with red")
    print("The path from {} to {} is evidenced by red edges".format(nodes[0],nodes[-1]))
    
    plt.figure(num=None, figsize=(15, 15),dpi=60)
    H = dg.subgraph(nodes)
    path=[]
    cont=0
    for u in H.nodes:
        if u==nodes[0] or u==nodes[-1]:
            path.append("red")
        else:
            path.append("blue")
    pos = nx.spring_layout(H)
    
    edge_colors = ['red' if e in p else "black"   for e in H.edges()] 
    #pos = nx.circular_layout(H)
    
    nx.draw(H, pos,with_labels=True,edge_color=edge_colors, connectionstyle='arc3, rad = 0.1',arrowsize=30,node_size=2100)
    nx.draw_networkx_nodes(H, pos,node_color=path)
    edge_labels = nx.get_edge_attributes(H,'weight')
    
    diz={}
    for u,v in edge_labels:
        diz[(u,v)]=edge_labels[(u,v)]
        
    nx.draw_networkx_edges(H, pos, width=1,style="dotted",edge_color="white")
    nx.draw_networkx_edge_labels(H, pos, edge_labels = diz,label_pos=0.2,font_size=20)
    
    plt.show()

