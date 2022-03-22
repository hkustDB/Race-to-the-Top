# -*- coding: utf-8 -*-
import sys
import os
import multiprocessing
manager = multiprocessing.Manager()



def main(argv):
    repeat_time = 10
    threads_num = 5
    global Data
    global Q
    global max_degree
    global q_pow
    global queries
    global times
    global results
    cur_path=os.getcwd()
    Data = manager.list()
    Q = manager.list()
    max_degree = manager.list()
    q_pow = manager.list()
    Q = ["one_path","triangle","two_path", "rectangle"]
    Data = ["Amazon2","Amazon1","RoadnetPA","RoadnetCA","Deezer"]
    max_degree = [1024,512,16,16,512]
    q_pow = [1,2,2,3]
    queries = manager.list()
    times = manager.list()
    results = manager.list()
    for i in range(len(Data)):
        time_i = manager.list()
        result_i = manager.list()
        query_i = manager.list()
        for j in range(len(Q)):
            time_i_j = manager.list()
            result_i_j = manager.list()
            for k in range(8):
                time_i_j_k = 0.0
                result_i_j_k = manager.list()
                time_i_j.append(time_i_j_k)
                result_i_j.append(result_i_j_k)
            time_i.append(time_i_j)
            result_i.append(result_i_j)
            query_i.append(0)
        times.append(time_i)
        results.append(result_i)
        queries.append(query_i)
    #Assign works to threads
    assigned_i = []
    assigned_j = []
    assigned_k = []
    for i in range(threads_num):
        assigned_i.append([])
        assigned_j.append([])
        assigned_k.append([])
    start_id = 0
    for i in range(len(Data)):
        if i==4:
            continue
        for j in range(len(Q)):
            if j!=3:
                continue
            for k in range(8):
                if k!=3:
                    continue
                for f in range(repeat_time):
                    assigned_i[start_id].append(i)
                    assigned_j[start_id].append(j)
                    assigned_k[start_id].append(k)
                    start_id = (start_id+1)%threads_num
    threads = []
    for i in range(threads_num):
        threads.append(multiprocessing.Process(target=ThreadWork,args=(i,assigned_i[i],assigned_j[i],assigned_k[i],cur_path)))
    for i in range(threads_num):
        threads[i].start()
    for i in range(threads_num):
        threads[i].join()
    for i in range(len(Data)):
        if i==4:
            continue
        for j in range(len(Q)):
            if j!=3:
                continue
            output_file = cur_path+"/../Result/Graph/R2TOld_"+str(Q[j])+"_"+Data[i]+".txt"
            output = open(output_file, 'w')
            for k in range(8):
                if k!=3:
                    continue
                print(str(i)+" "+str(j)+" "+str(k))
                times[i][j][k] /= repeat_time
                results[i][j][k].sort()
                res = sum(results[i][j][k])-results[i][j][k][0]-results[i][j][k][1]-results[i][j][k][repeat_time-1]-results[i][j][k][repeat_time-2]
                res = res/(repeat_time-4)
                output.write(str(pow(2,k)*0.1)+" "+str(times[i][j][k])+"\n")
                
   
                
def ThreadWork(thread_id,assigned_i,assigned_j,assigned_k,cur_path):
    global Data
    global Q
    global max_degree
    global q_pow
    global queries
    global times
    global results
    work_num = len(assigned_i)
    for l in range(work_num):
        i = assigned_i[l]
        j = assigned_j[l]
        k = assigned_k[l]
        print(str(i)+" "+str(j)+" "+str(k))
        #Create a new file
        cmd = "cp "+cur_path+"/../Information/Graph/"+Q[j]+"/"+Data[i]+".txt "+cur_path+"/../Temp/Old"+Q[j]+"_"+Data[i]+"_"+str(thread_id)+".txt"
        shell = os.popen(cmd, 'r')
        shell.read()
        shell.close()
        #Collect the result for algorithm
        cmd = "python "+cur_path+"/../Code/R2TOld.py -I "+cur_path+"/../Temp/Old"+Q[j]+"_"+Data[i]+"_"+str(thread_id)+".txt"
        cmd = cmd+" -b 0.1 -e "+str(pow(2,k)*0.1)+" -G "+str(pow(max_degree[i],q_pow[j]))+" -p 10"
        shell = os.popen(cmd, 'r')
        res = shell.read()
        res = res.split()
        a = float(res[2])
        b = float(res[5])
        c = float(res[7])
        results[i][j][k].append(abs(a-b))        
        queries[i][j] = a
        times[i][j][k] = times[i][j][k]+c
        shell.close()
        #Remove the new file
        cmd = "rm "+cur_path+"/../Temp/Old"+Q[j]+"_"+Data[i]+"_"+str(thread_id)+".txt"
        shell = os.popen(cmd, 'r')
        shell.read()
        shell.close()  
    
    
    
if __name__ == "__main__":
	main(sys.argv[1:])
    
