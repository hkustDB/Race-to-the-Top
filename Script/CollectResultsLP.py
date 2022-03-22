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
    LP_time = {}
    LP_over_time = {}
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
            LP_time[tau] = float(60*60*6)
            LP_res[tau] = float(10000000000)
            LP_over_time[tau] = True
            tau/=2
            ii+=1
            continue
        l1 = lines[ii*4+1]
        l2 = lines[ii*4+2]
        l3 = lines[ii*4+3]
        elements = l1.split()
        LP_time[tau] = float(elements[1])
        elements = l2.split()
        res = float(elements[2])
        elements = l3.split()
        LP_res[tau] = float(elements[2])
        LP_over_time[tau] = False
        tau/=2
        ii+=1
    output_file = cur_path+"/../Result/Graph/LP_"+str(Q[j])+"_"+Data[i]+".txt"
    output = open(output_file, 'w')
    for k in range(8):
        fail_time = 0
        err = []
        e = 0.1*pow(2,k)
        total_time = 0
        for j in range(repeat_time):
            a = random.uniform(0,1)
            tau = tau_list[int(a*len(tau_list))]
            total_time += LP_time[tau]/repeat_time
            if LP_over_time[tau]==True:
                fail_time +=1
                err.append(abs(res-LP_res[tau]-LapNoise()*tau/e)/repeat_time)
            else:
                err.append(abs(res-LP_res[tau]-LapNoise()*tau/e)/repeat_time)
        err.sort()
        if fail_time<int(repeat_time*0.2):
            fail_time = int(repeat_time*0.2)
        if fail_time>int(repeat_time*0.45):
            print("error")
            fail_time = int(repeat_time*0.48)
        #First divide repeat_time and then multiply is to avoid the result too large to overflow
        total_err = sum(err[fail_time:repeat_time-fail_time])/(repeat_time-2*fail_time)*repeat_time
        output.write(str(pow(2,k)*0.1)+" "+str(res)+" "+str(total_err)+" "+str(total_time)+"\n")
    
    
    
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
        for j in range(len(Q)):
            Process(i,j, cur_path)
    
    
    
if __name__ == "__main__":
	main(sys.argv[1:])

