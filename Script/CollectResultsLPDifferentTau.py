# -*- coding: utf-8 -*-
import sys
import os
import random
import math



def LapNoise():
    a = random.uniform(0,1)
    b = math.log(1/(1-a))
    c = random.uniform(0,1)
    if c>0.5:
        return b
    else:
        return -b
    
    
def Process(i,j, cur_path):
    global Q
    global max_degree
    global q_pow
    global Data
    repeat_time = 100
    input_file_path = cur_path+"/../Result/Graph/LP_All_Tau_"+str(Q[j])+"_"+Data[i]+".txt"
    input_file = open(input_file_path, 'r')
    LP_res = {}
    res = 0
    lines = input_file.readlines()
    GS = pow(max_degree[i],q_pow[j])
    ii = 0
    tau = GS
    num_line = len(lines)
    tau_list = []
    while(tau>=2):
        tau_list.append(tau)
        if ii*4+3>num_line:
            LP_res[tau] = float(10000000000)
            tau/=2
            ii+=1
            continue
        l2 = lines[ii*4+2]
        l3 = lines[ii*4+3]
        elements = l2.split()
        res = float(elements[2])
        elements = l3.split()
        LP_res[tau] = float(elements[2])
        tau/=2
        ii+=1
    tau = GS
    for i in range(7):
        err = []
        e = 0.8
        total_err = 0
        if tau<2:
            total_err =res- res/(q_pow[j]+1)*tau
        else:
            for i in range(repeat_time):
                err.append(abs(res-LP_res[tau]-LapNoise()*tau/e)/(repeat_time-int(repeat_time*0.4)))
            total_err = sum(err[int(repeat_time*0.2):repeat_time-int(repeat_time*0.2)])
        tau/=8
        print(Q[j]+" "+str(tau)+" "+str(total_err))
    


def main(argv):
    global Q
    global max_degree
    global q_pow
    global Data
    cur_path=os.getcwd()
    Q = ["one_path","triangle","two_path", "rectangle"]
    Data = ["Amazon2","Amazon1","RoadnetPA","RoadnetCA","Deezer"]
    max_degree = [1024,1024,16,16,1024]
    q_pow = [1,2,2,3]
    for i in range(len(Data)):
        if i!=0:
            continue
        for j in range(len(Q)):
            Process(i,j, cur_path)
    
    
    
if __name__ == "__main__":
	main(sys.argv[1:])