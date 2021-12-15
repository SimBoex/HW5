
def find_min(l,dG):
    mi=[]
    for edge in l:
        diz=dG.get_edge_data(*edge)
        cost=diz["weight"]
        mi.append((edge,cost))
    mi=sorted(mi,key= lambda x : x[1])
    return mi[0][0]    



#it computes the number of edges we need to remove( considering their weights)
def Min_cut(G,user1,user2,startingTime,endTime):
    G=new_graph(G,startingTime,endTime)
    cost=0
    edges=[]
    while path:
        pred=dijkstra(user1,user2,G,startingTime,endTime)
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