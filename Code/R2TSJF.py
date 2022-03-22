# -*- coding: utf-8 -*-
import getopt
import math
import sys
import random
import time



def ReadInput():
    global input_file_path
    global size_dic
    global real_query_result
    real_query_result = 0
    size_dic = {}
    input_file = open(input_file_path,'r')
    for line in input_file.readlines():
        elements = line.split()
        value = float(elements[0])
        entity = int(elements[1])
        real_query_result += value
        if entity in size_dic.keys():
            size_dic[entity] += value
        else:
            size_dic[entity] = value
    
    
    
def LapNoise():
    a = random.uniform(0,1)
    b = math.log(1/(1-a))
    c = random.uniform(0,1)
    if c>0.5:
        return b
    else:
        return -b



def RunAlgorithm():
    global global_sensitivity
    global beta
    base = 5.5
    max_i = int(math.log(global_sensitivity,base))
    if max_i<=1:
        max_i+=1
    max_res1 = -10000000
    for i in range(1,max_i+1):
        tau = math.pow(base,i)
        t_res2 = LP(tau)+LapNoise()*math.pow(base,i)/epsilon*max_i
        t_res1 = t_res2 - math.pow(base,i)/epsilon*max_i*math.log(max_i/beta,2.9718)
        if t_res1>max_res1:
            max_res1 = t_res1
    return max_res1
    
    

def LP(tau):
    global size_dic
    res = 0
    for element in size_dic.keys():
        res += min(tau,size_dic[element])
    return res



def main(argv):
    #The input file including the relationships between aggregations and base tuples
    global input_file_path
    input_file_path = ""
    #Privacy budget
    global epsilon
    epsilon = 0.1
    #Error probablity: with probablity at least 1-beta, the error can be bounded
    global beta
    beta = 0.1
    #The global sensitivity
    global global_sensitivity
    global real_query_result
    global_sensitivity = 1000000
    try:
        opts, args = getopt.getopt(argv,"h:I:e:b:G:",["Input=","epsilon=","beta=","GlobalSensitivity="])
    except getopt.GetoptError:
        print("R2TSJF.py -I <input file> -e <epsilon(default 0.1)> -b <beta(default 0.01)> -G <global sensitivity(default 1000,000)>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("R2TSJF.py -I <input file> -e <epsilon(default 0.1)> -b <beta(default 0.01)> -G <global sensitivity(default 1000,000)")
            sys.exit()
        elif opt in ("-I", "--Input"):
            input_file_path = str(arg)
        elif opt in ("-e","--epsilon"):
            epsilon = float(arg)
        elif opt in ("-b","--beta"):
            beta = float(arg)
        elif opt in ("-G","--GlobalSensitivity"):
            global_sensitivity = float(arg)
    start = time.time()
    ReadInput()
    res = RunAlgorithm()
    end= time.time()
    print("Query Result")
    print(real_query_result)
    print("Noised Result")
    print(res)
    print("Time")
    print(end-start)
    
	

if __name__ == "__main__":
	main(sys.argv[1:])
