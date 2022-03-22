# -*- coding: utf-8 -*-
import sys
import getopt
import cplex
import numpy as np
import time
import os



def main(argv):
    global Data
    global Q
    global max_degree
    global q_pow
    global queries
    global times
    global results
    global results_enhanced
    global cur_path
    global time_repeat
    global error_repeat
    time_repeat = 10
    cur_path=os.getcwd()
    Q = ["one_path","triangle","two_path", "rectangle"]
    Data = ["Amazon2","Amazon1","RoadnetPA","RoadnetCA","Deezer"]
    max_degree = [1024,1024,16,16,1024]
    q_pow = [1,2,2,3]
    i=0
    j=0
    try:
        opts, args = getopt.getopt(argv,"h:Q:D:",["QueryId=","DataId="])
    except getopt.GetoptError:
        print("CollectResultsLPAllTau.py -Q <Query Id: 0(one_path)/1(triangle)/2(two_path)/3(rectangle)> -D <Data Id: 0(Amazon2)/1(Amazon1)/2(RoadnetPA)/3(RoadnetCA)/4(Deezer)>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("CollectResultsLPAllTau.py -Q <Query Id: 0(one_path)/1(triangle)/2(two_path)/3(rectangle)> -D <Data Id: 0(Amazon2)/1(Amazon1)/2(RoadnetPA)/3(RoadnetCA)/4(Deezer)>")
            sys.exit()
        elif opt in ("-Q", "--QueryId"):
            j = int(arg)
        elif opt in ("-D", "--DataId"):
            i = int(arg)
    Process(i,j,cur_path)
            


def ReadInput(input_file_path):
    global tuples
    global connections
    global downward_sensitivity
    global real_query_result
    size_dic = {}
    id_dic = {}
    id_num = 0
    real_query_result = 0
    #Collect the DS
    downward_sensitivity = 0
    #The variable is repsented one entity
    #We use connection to show the connections between entity and query results
    tuples = []
    connections = []
    input_file = open(input_file_path,'r')
    for line in input_file.readlines():
        real_query_result += 1
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
    
    

def LPSolver(tau):
    global tuples
    global connections
    global real_query_result
    num_constraints = len(tuples)
    num_variables = len(connections)
    # Set the obj
    cpx = cplex.Cplex()
    cpx.set_log_stream(None)
    cpx.set_error_stream(None)
    cpx.set_warning_stream(None)
    cpx.set_results_stream(None) 
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
    cpx.solve()
    return cpx.solution.get_objective_value()


    
def Process(i,j,cur_path):
    global time_repeat
    global error_repeat
    global real_query_result
    ReadInput(cur_path+"/../Information/Graph/"+Q[j]+"/"+Data[i]+".txt")
    GS = pow(max_degree[i],q_pow[j])
    tau = GS
    while(tau>=2):
        print(str(tau))
        used_time = 0
        res = 0
        for ii in range(time_repeat):
            start = time.time()
            res = LPSolver(tau)    
            end= time.time()
            used_time+=end-start
        used_time/=time_repeat
        print("Time: "+str(used_time))
        print("Query result: "+str(real_query_result))
        print("LP result: "+str(res))
        tau/=2


if __name__ == "__main__":
	main(sys.argv[1:])