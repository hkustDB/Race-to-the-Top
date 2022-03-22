# -*- coding: utf-8 -*-
import getopt
import math
import sys
import random
import cplex
import numpy as np
import time
import multiprocessing
manager = multiprocessing.Manager()


def ReadInput():
    global input_file_path
    global tuples
    global connections
    global downward_sensitivity
    size_dic = {}
    id_dic = {}
    id_num = 0
    #Collect the DS
    downward_sensitivity = 0
    #The variable is repsented one entity
    #We use connection to show the connections between entity and query results
    tuples = []
    connections = []
    input_file = open(input_file_path,'r')
    for line in input_file.readlines():
        elements = line.split()
        connection = []
        for element in elements[1:]:
            element = int(element)
            #Re-order the IDs
            if element in id_dic.keys():
                element = id_dic[element]
            else:
                tuples.append(id_num)
                id_dic[element] = id_num
                element = id_num
                id_num+=1                
            if element in size_dic.keys():
                size_dic[element]+=1
            else:
                size_dic[element] = 1
            if downward_sensitivity<=size_dic[element]:
                downward_sensitivity = size_dic[element];                
            connection.append(element)
        connections.append(connection)
      
        

def LapNoise():
    a = random.uniform(0,1)
    b = math.log(1/(1-a))
    c = random.uniform(0,1)
    if c>0.5:
        return b
    else:
        return -b
    
      
        
def ThresholdRunAlgorithm(epsilon,beta,base, max_i, downward_sensitivity, real_query_result, assigned_taus):
    global tilde_Q_tau
    global Q_tau
    global hat_Q_tau
    for i in assigned_taus:
        tau = math.pow(base,i)
        if tau>=downward_sensitivity:
            t_res = real_query_result
        else:   
            t_res = LPSolver(tau)
        Q_tau[i] = t_res
        hat_Q_tau[i] = t_res+LapNoise()*tau/epsilon*max_i
        tilde_Q_tau[i] = hat_Q_tau[i]-tau/epsilon*max_i*math.log(max_i/beta,2.9718)
        
    

def RunAlgorithm():
    global global_sensitivity
    global connections
    global downward_sensitivity
    global tilde_Q_tau
    global Q_tau
    global hat_Q_tau
    global epsilon
    global beta
    global real_query_result
    
    base = 5.5
    max_i = int(math.log(global_sensitivity,base))
    if max_i<=1:
        max_i+=1
    real_query_result = len(connections)

    #Used to store the results
    Q_tau = manager.dict()
    tilde_Q_tau = manager.dict()
    hat_Q_tau = manager.dict()
    
    #Assign the tau's
    arrangement_of_taus = []
    for i in range(processor_num):
        arrangement_of_taus.append([])
    
    j = 0
    for i in range(1,max_i+1):
        arrangement_of_taus[j].append(i)
        j = (j+1)%processor_num
        Q_tau[i] = 0
        tilde_Q_tau[i] = 0
        hat_Q_tau[i] = 0
    
    threads = []
    for i in range(processor_num):
        threads.append(multiprocessing.Process(target=ThresholdRunAlgorithm, args=(epsilon,beta,base, max_i, downward_sensitivity, real_query_result, arrangement_of_taus[i])))    
        threads[i].start()
    for i in range(processor_num):
        threads[i].join()
    
    max_ind = 1
    max_val = 0
    for i in range(1,max_i+1):
        if tilde_Q_tau[i]>max_val:
            max_val = tilde_Q_tau[i]
            max_ind = i
    final_res = tilde_Q_tau[max_ind]
    return final_res

      

def LPSolver(tau):
    global tuples
    global connections
    num_constraints = len(tuples)
    num_variables = len(connections)
    
    # Set the obj
    cpx = cplex.Cplex()
    cpx.objective.set_sense(cpx.objective.sense.maximize)

    #Set variables
    obj = np.ones(num_variables)
    ub = np.ones(num_variables)
    cpx.variables.add(obj=obj, ub=ub)
    
    #Set the right hand side and the sign
    rhs = np.ones(num_constraints)*tau
    senses = "L" * num_constraints
    cpx.linear_constraints.add(rhs=rhs, senses=senses)
    
    #Set the coefficients
    cols = []
    rows = []
    vals = []
    
    for i in range(num_variables):
        for j in connections[i]:
            cols.append(i)
            rows.append(j)
            vals.append(1)
    cpx.linear_constraints.set_coefficients(zip(rows, cols, vals))
    cpx.set_log_stream(None)
    cpx.set_error_stream(None)
    cpx.set_warning_stream(None)
    cpx.set_results_stream(None)
    cpx.solve()
    return cpx.solution.get_objective_value()    


def main(argv):
    global input_file_path
    global epsilon
    global beta
    global global_sensitivity
    global processor_num
    global real_query_result
    processor_num = 1
	
    try:
        opts, args = getopt.getopt(argv,"h:I:e:b:G:p:",["Input=","epsilon=","beta=","GlobalSensitivity=","ProcessorNum="])
    except getopt.GetoptError:
        print("R2TOld.py -I <input file> -e <epsilon> -b <beta> -G <global sensitivity> -p <processor number>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("R2TOld.py -I <input file> -e <epsilon> -b <beta> -G <global sensitivity> -p <processor number>")
            sys.exit()
        elif opt in ("-I", "--Input"):
            input_file_path = str(arg)
        elif opt in ("-e","--epsilon"):
            epsilon = float(arg)
        elif opt in ("-b","--beta"):
            beta = float(arg)
        elif opt in ("-G","--GlobalSensitivity"):
            global_sensitivity = float(arg)
        elif opt in ("-p","--ProcessorNum"):
            processor_num = int(arg)
    if processor_num <1:
        processor_num = 1
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