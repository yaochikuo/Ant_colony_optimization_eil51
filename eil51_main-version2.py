import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
#import math
import os

alpha=1.0
beta=1.1
tho=0.95
pop_size=50
dist_limit=30
iter_times=1000
top_select=30

#cur_path=os.path.dirname(__file__)
#cur_path
df = pd.read_csv('d:/Desktop/python code/Ant_colony_optimization_eil51/eil51.csv')
#df = pd.read_csv('d:/Desktop/eil51/eil51.csv')
x=np.array(df.x)
x
y=np.array(df.y)


dij=np.array([[((x[i]-x[j])**2+(y[i]-y[j])**2)**0.5 for j in range(len(x))] for i in range(len(x))])


def find_nearest(list_1d,node_num):
    min_dist=99999
    for i in list_1d:
        r=((x[i]-x[node_num])**2+(y[i]-y[node_num])**2)**0.5
        if (r<min_dist):
            min_dist=r
            index=i
    return index

def get_routine_dist(path_list): #len(path_list) = 52
    routine_dist=0
    for i in range(1,len(path_list)):
        r=((x[path_list[i]]-x[path_list[i-1]])**2+(y[path_list[i]]-y[path_list[i-1]])**2)**0.5
        routine_dist=routine_dist+r
    return routine_dist

def gen_rand_path():
    list_1d_random=[i for i in range(51)]
    rand_path=[]
    for i in range(51):
        #rand=random.randint(0,len(list_1d_random)-1)
        city=list_1d_random[random.randint(0,len(list_1d_random)-1)]
        #print(random.randint(0,len(list_1d_random)))
        rand_path.append(city)
        list_1d_random.remove(city)
        #print(i,city)
    #print(len(city_random_path))
    rand_path.append(rand_path[0])
    #print(len(city_random_path))
    return rand_path

def gen_path_by_dist(ini_node):
    a_list=[i for i in range(51)]
    path=[ini_node]
    a_list.remove(ini_node)
    city=ini_node
    for i in range(50):
        city=find_nearest(a_list,city)
        a_list.remove(city)
        #print("city=",city)
        path.append(city)
        
    
    #print("city_path=",city_path)
    #print("city_len=",len(city_path))
    path.append(ini_node)
    return path

#random a start position
def construct_a_path():
    ini_city=random.randint(0,50)
    #ini_city=39
    path3=[ini_city]
    allowed_city_list=[i for i in range(51)]
    #print("ini_city",ini_city)
    allowed_city_list.remove(ini_city)
    #print(allowed_city_list)
    for i in range(50):
        P_sum=0
        for j_city in allowed_city_list:
            P_sum=P_sum+pheromone[ini_city][j_city]**alpha*(1.0/dij[ini_city][j_city])**beta
        
        rand=random.random()
        #print("rand=",rand)
        P=0.0    
        for j_city in allowed_city_list:    
            P=P+pheromone[ini_city][j_city]**alpha*(1.0/dij[ini_city][j_city])**beta/P_sum
            #print("ini_city=%2d,j_city=%2d,P=%9.7f P_sum=%9.7f" %(ini_city,j_city,P,P_sum))
            if P>rand:
                path3.append(j_city)
                allowed_city_list.remove(j_city)
                ini_city=j_city
                #print("selected j_city",j_city)
                break
    path3.append(path3[0])
    

    return path3

#plot a path
def plotpath(a_path,file_num):
    a_path_x=[]
    a_path_y=[]
    for i in range(len(a_path)):
        a_path_x.append(x[a_path[i]])
        a_path_y.append(y[a_path[i]])
    
    
    
    plt.scatter(x,y)
    plt.scatter(x[a_path[-1]],y[a_path[-1]])
    plt.scatter(x[a_path[-2]],y[a_path[-2]],color='r')
    plt.plot(a_path_x,a_path_y)
    plt.title("T%05d" %(file_num))
    plt.xlim(0,70)
    plt.ylim(0,80)
    num=get_routine_dist(a_path)
    filename=(r"%3d.%04d" %(int(num),(num-int(num))*10000))
    plt.text(50,75,"dist=%s" %(filename))
    #aaa=str(get_routine_dist(a_path))
    print("file=",filename)
    #'./img/testols.png'
    plt.savefig('./%s/%s.png' %(folder,filename))
    
    plt.show()
    
    
    return

def write_file(a_path,file_num):

    num=get_routine_dist(a_path)
    filename=(r"%3d.%04d" %(int(num),(num-int(num))*10000))
    f=open('./%s/%s.txt' %(folder,filename),'w')
    
    for city in a_path:
        f.write("%3d %f %f\n"  %(city,x[city],y[city]))
    
    
    f.close()
    return
    

def update_pheromone(curr_arr):
    global pheromone
    global Q
    Q=1.0
    #pheromone=[[pheromone[i][j]*0.9 for j in range(51)] for i in range(51)]
    #pheromone=np.array(pheromone)
    #pheromone=pheromone*tho
    
    tmp_arr=[[curr_arr[i][j] for j in range(len(curr_arr[0]))] for i in range(len(curr_arr))]
    path_record=[]
    for j in range(len(tmp_arr)):
        path_record.append(get_routine_dist(tmp_arr[j]))
    
    
    an_arr=[]
    for i in range(top_select):
        index=path_record.index(min(path_record))
        an_arr.append(tmp_arr[index])
        path_record.pop(index)
    
    
    pheromone=pheromone*tho
    
    #print("an_arr",len(an_arr),len(an_arr[0]))
    
    
    
    for kk in range(len(an_arr)):
    
        for k in range(len(an_arr[0])-1):
            i=an_arr[kk][k]
            j=an_arr[kk][k+1]
            pheromone[i][j] = pheromone[i][j] + Q/dij[i][j]
            pheromone[j][i] = pheromone[i][j]
        #print("q/dij=%9.7f" %(Q/dij[i][j]))
        #print("i=%2d  dij=%9.7f Q/dij=%9.7f phe_=%9.7f" %(k,dij[i][j],Q/dij[i][j],pheromone[i][j]) )
        
#    for i in range(51):
#        for j in range(51):
#            if pheromone[i][j] <0.0002:
#                pheromone[i][j]=0.0002
    
    for i in range(51):
        for j in range(51):
            if dij[i][j] >dist_limit:
                pheromone[i][j]=0.0
        
    return


def ini_pheromone():
    global pheromone
    pheromone=[[1.0 for j in range(51)] for i in range(51)]
    pheromone = np.array(pheromone)
    pheromone.shape
    for i in range(51):
        for j in range(51):
            if dij[i][j] >dist_limit:
                pheromone[i][j]=0.0


    return

""" main """




for k in range(31,10000):
    
    folder=("test%05d" %(k))
    os.mkdir(folder)
    
    #initialize pheromone table
    ini_pheromone()
    
   
    
    
    best_dist_value=9999999
    
    
    trend=[]
    
    
    
    
    for i in range(iter_times):
        
        curr=[]
        #construct pop_size * path
        for j in range(pop_size):
            tmp_path=construct_a_path()
            while (len(tmp_path)<52 or dij[tmp_path[-1]][tmp_path[-2]]>dist_limit   ):
                tmp_path=construct_a_path()
            curr.append(tmp_path)
        
        # update pheromone
        #pheromone=pheromone*tho
        #for j in range(pop_size):
        update_pheromone(curr) 
    
        
        # record path dist
        path_record=[]
        for j in range(len(curr)):
            path_record.append(get_routine_dist(curr[j]))
        
        
        #best_dist_value=min(path_record)
        
        index=path_record.index(min(path_record))
        
        #best path
        best_path=curr[index]
        
        
      
    
        
        if min(path_record) < best_dist_value:
            best_dist_value=min(path_record)
            print("index=",index)
            plotpath(best_path,i)
            write_file(best_path,i)
        trend.append(best_dist_value)    
        
        print("routine dist=",i,best_dist_value)
    
    
    
    
    
    
    print(pheromone)
    print(type(pheromone))
    print(pheromone.shape)
    print("best_path=",best_path)
    print("len(best_path)=",len(best_path))
    print("routine dist=",get_routine_dist(best_path))
    plt.plot(trend)
    plt.savefig('./%s/trend.png' %(folder))
    
    f=open('./%s/trend.txt' %(folder),'w')
    for i in range(len(trend)):
        f.write('%d %f\n' %(i,trend[i]))
    
    f.close()
    
    
    #plotpath(best_sol)
    #print(dij)


