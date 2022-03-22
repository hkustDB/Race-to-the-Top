# -*- coding: utf-8 -*-
import sys
import getopt
import cplex
import numpy as np
import math
import time
import random



def LapNoise():
    a = random.uniform(0,1)
    b = math.log(1/(1-a))
    c = random.uniform(0,1)
    if c>0.5:
        return b
    else:
        return -b
    
    

def ReadInput():
    global input_file_path
    global tuples
    global connections
    id_dic = {}
    id_num = 0

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
            connection.append(element)
        connections.append(connection)
    

    
def RunHLP(num):
    global tuples
    global connections
    num_tuples = len(tuples)
    num_connections = len(connections)
    
	# Set the obj
    cpx = cplex.Cplex()
    cpx.objective.set_sense(cpx.objective.sense.minimize)
    
    cpx.set_log_stream(None)
    cpx.set_error_stream(None)
    cpx.set_warning_stream(None)
    cpx.set_results_stream(None) 
    
    #Set variables
    obj = np.append(np.zeros(num_tuples),np.ones(num_connections))
    ub = np.append(np.ones(num_tuples),np.array([cplex.infinity] * num_connections))
    cpx.variables.add(obj=obj, ub=ub)
    
    #Generate the constriants
    #Three types of constraints: 
    #1. Constriants between query results and tuples. There are num_connections such constraints
    #2. Non-negative constraints for query results
    #3. Make the sum of all tuples equal to num
    rhs = np.zeros(2*num_connections+2)
    cols = []
    rows = []
    vals = []
    senses = "L" * (2*num_connections+2)
    
    #The first type of constraints
    for i in range(num_connections):
        temp_list = list(set(connections[i]))
        rhs[i] = len(temp_list)-1
        rows.append(i)
        cols.append(num_tuples+i)
        vals.append(-1)
        for j in temp_list:
            rows.append(i)
            cols.append(j)
            vals.append(1)
            
    #The second type of constraints
    for i in range(num_connections):
        rhs[i+num_connections] = 0
        rows.append(i+num_connections)
        cols.append(num_tuples+i)
        vals.append(-1)
    
    #The third type of constraints
    rhs[2*num_connections] = num
    for i in range(num_tuples):
        rows.append(2*num_connections)
        cols.append(i)
        vals.append(1)
    rhs[2*num_connections+1] = -1*num
    for i in range(num_tuples):
        rows.append(2*num_connections+1)
        cols.append(i)
        vals.append(-1)
        
    cpx.linear_constraints.add(rhs=rhs, senses=senses)
    cpx.linear_constraints.set_coefficients(zip(rows, cols, vals))
    cpx.solve()
    return cpx.solution.get_objective_value()
        
    
    
def RunGLP(num):
    global tuples
    global connections
    num_tuples = len(tuples)
    num_connections = len(connections)
    
    # Set the obj
    cpx = cplex.Cplex()
    cpx.objective.set_sense(cpx.objective.sense.minimize)
    
    cpx.set_log_stream(None)
    cpx.set_error_stream(None)
    cpx.set_warning_stream(None)
    cpx.set_results_stream(None) 
    
    #Set variables
    obj = np.append(np.zeros(num_tuples+num_connections),np.ones(1))
    ub = np.append(np.ones(num_tuples),np.array([cplex.infinity] * (num_connections+1)))
    cpx.variables.add(obj=obj, ub=ub)

    #Generate the constriants
    #Three types of constraints: 
    #1. Constriants between query results and tuples. There are num_connections such constraints
    #2. Non-negative constraints for query results
    #3. Make the sum of all tuples equal to num
    #4. The sensitivity should be less than the sensitivity for any tuple
    rhs = np.zeros(2*num_connections+2+num_tuples)
    cols = []
    rows = []
    vals = []
    senses = "L" * (2*num_connections+2+num_tuples)
    
    #The first type of constraints
    for i in range(num_connections):
        temp_list = list(set(connections[i]))
        rhs[i] = len(temp_list)-1
        rows.append(i)
        cols.append(num_tuples+i)
        vals.append(-1)
        for j in temp_list:
            rows.append(i)
            cols.append(j)
            vals.append(1)
    
    #The second type of constraints
    for i in range(num_connections):
        rhs[i+num_connections] = 0
        rows.append(i+num_connections)
        cols.append(num_tuples+i)
        vals.append(-1)
    
    #The third type of constraints
    rhs[2*num_connections] = num
    for i in range(num_tuples):
        rows.append(2*num_connections)
        cols.append(i)
        vals.append(1)
    rhs[2*num_connections+1] = -1*num
    for i in range(num_tuples):
        rows.append(2*num_connections+1)
        cols.append(i)
        vals.append(-1)
    
    #The fourth type of constraints
    for i in range(num_tuples):
        rows.append(2*num_connections+2+i)
        cols.append(num_tuples+num_connections)
        vals.append(-1)
        rhs[2*num_connections+2+i] = 0
    for i in range(num_connections):
        temp_list = list(set(connections[i]))
        for j in temp_list:
            rows.append(2*num_connections+2+j)
            cols.append(num_tuples+i)
            vals.append(1)
    
    cpx.linear_constraints.add(rhs=rhs, senses=senses)
    cpx.linear_constraints.set_coefficients(zip(rows, cols, vals))
    cpx.solve()
    return cpx.solution.get_objective_value()



def RunRecursive():
    global tuples
    global connections
    global epsilon
    global delta  
    num_tuples = len(tuples)
    
    #Find the Delta
    left_i = 0
    right_i = num_tuples
    beta = epsilon/math.log2(1/delta)
    while right_i-left_i>1:
        mid_i = int((left_i+right_i)/2)
        temp_x = RunGLP(num_tuples-mid_i)
        if temp_x <=0:
            temp_x = -10000000
        else:
            temp_x = math.log(temp_x,math.e)
        temp_y = mid_i*beta
        if temp_x >= temp_y:
            left_i = mid_i
        else:
            right_i = mid_i
    delta = math.pow(math.e,right_i*beta)
    delta =  delta*math.pow(math.e,1+beta/epsilon*LapNoise())
    
    #Find the optimal 
    left_i = 0
    right_i = num_tuples
    while right_i-left_i>1:
        mid_i = int((left_i+right_i)/2)
        a_value = 0
        b_value = 0
        if mid_i-1>=0:
            a_value = RunHLP(mid_i-1)+(num_tuples-mid_i+1)*delta
        else:
            a_value = RunHLP(0)+(num_tuples)*delta
        b_value = RunHLP(mid_i)+(num_tuples-mid_i)*delta
        
        if b_value<=a_value:
            left_i = mid_i
        else:
            right_i = mid_i   
    l_value = RunHLP(left_i)+(num_tuples-left_i)*delta
    r_value = RunHLP(right_i)+(num_tuples-right_i)*delta
    res = 0
    if l_value<r_value:
        res = l_value
    else:
        res = r_value
    res = res+LapNoise()*delta/epsilon
    
    print("Query Result")
    print(len(connections))
    print("Noised Result")
    print(res)



def main(argv):
    global input_file_path
    global epsilon
    global delta   
    
    try:
        opts, args = getopt.getopt(argv,"I:e:d:",["Input=","epsilon=","delta="])
    except getopt.GetoptError:
        print("RM.py -I <input file> -e <epsilon> -d <delta>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("RM.py -I <input file> -e <epsilon> -d <delta>")
            sys.exit()
        elif opt in ("-I", "--Input"):
            input_file_path = arg
        elif opt in ("-e","--epsilon"):
            epsilon = float(arg)*0.5
        elif opt in ("-d","--delta"):
            delta = float(arg)
    
    start = time.time()
    ReadInput()
    RunRecursive()
    end= time.time()
    print("Time")
    print(end-start)


if __name__ == "__main__":
   main(sys.argv[1:])
