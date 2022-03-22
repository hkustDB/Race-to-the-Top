# -*- coding: utf-8 -*-
import sys
import os
import time



def main(argv):
    Q = [5,8,21,3,12,20,10,7,11,18]
    P = ["ids","ids","ids","customer","orders","supplier","customer","ids","supplier","customer"]
    DB = ["sc","sc","so","sc","sc","sc","sc","sc","sc","sc"]
    S = ["0","1","2","3","4","5","6","7"]
    cur_path=os.getcwd()
    repeat_time = 10
    times = []
    for i in range(len(S)):
        time_i = []
        for j in range(len(Q)):
            time_i_j = 0.0
            for k in range(repeat_time):
                print(str(i)+" "+str(j)+" "+str(k))
                start = time.time()
                cmd = "python "+cur_path+"/../Code/ExtractInfo.py -D "+DB[j]+"_"+S[i]+" -Q "+cur_path+"/../Query/Q"+str(Q[j])+".txt -K "+cur_path+"/../Query/Q"+str(Q[j])
                cmd = cmd+"_key.txt -P "+P[j]+" -O "+cur_path+"/../Temp/temp.txt"
                shell = os.popen(cmd, 'r')
                shell.read()
                shell.close()
                end= time.time()
                time_i_j+=end-start
                cmd = "rm "+cur_path+"/../Temp/temp.txt"
                shell = os.popen(cmd, 'r')
                shell.read()
                shell.close()
            time_i_j /= repeat_time
            time_i.append(time_i_j)
        times.append(time_i)
    output_file = cur_path+"/../Result/TPCH/ExtractInfoTimeTPCH.txt"
    results = open(output_file, 'w')
    for i in range(len(S)):
        for j in range(len(Q)):
            results.write(S[i]+" Q"+str(Q[j])+" "+str(times[i][j])+"\n")
        
    
    
if __name__ == "__main__":
	main(sys.argv[1:])