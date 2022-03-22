# -*- coding: utf-8 -*-
import sys
import os



def main(argv):
    Q = [3,12,20]
    GS_L = [10000,10000,10000]
    repeat_time = 10
    cur_path=os.getcwd()
    for i in range(len(Q)):
        output_file = cur_path+"/../Result/TPCH/R2T_Q"+str(Q[i])+"_GS.txt"
        output = open(output_file, 'w')
        for j in range(8):
            print(str(i)+" "+str(j))
            GS = GS_L[i]*pow(10,j)
            results = []
            cmd = "python "+cur_path+"/../Code/R2TSJF.py -I "+cur_path+"/../Information/TPCH/Q"+str(Q[i])+"_3.txt -b 0.1 -e 0.8 -G "+str(GS)
            for k in range(repeat_time):
                shell = os.popen(cmd, 'r')
                res = shell.read()
                res = res.split()
                a = float(res[2])
                b = float(res[5])
                results.append(abs(a-b))
                shell.close()
            results.sort()  
            res = sum(results)-results[0]-results[1]-results[repeat_time-1]-results[repeat_time-2]
            res = res/(repeat_time-4)
            output.write(str(GS)+" "+str(res)+"\n")
        output.close()
            
    

if __name__ == "__main__":
	main(sys.argv[1:])