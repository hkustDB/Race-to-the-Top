# -*- coding: utf-8 -*-
import sys
import os
import psycopg2
import time


def main(argv):
    Q = [5,8,21,3,12,20,10,7,11,18]
    S = ["0","1","2","3","4","5","6"]
    DB = ["sc","sc","so","sc","sc","sc","sc","sc","sc","sc"]
    cur_path=os.getcwd()
    repeat_time = 10
    times = []
    for i in range(len(S)):
        time_i = []
        for j in range(len(Q)):
            time_i_j = 0.0
            con = psycopg2.connect(database=DB[j]+"_"+S[i])
            cur = con.cursor()
            query_path = cur_path+"/../Query/Q"+str(Q[j])+".txt"
            query = ""
            query_file = open(query_path,'r')
            # Read the query file and store in query
            for line in query_file.readlines():
                query = query + line
                if ";" in query:
                    query = query.replace('\n'," ")
                    break
            for k in range(repeat_time):
                print(str(i)+" "+str(j)+" "+str(k))
                start = time.time()
                cur.execute(query)
                cur.fetchall()
                end= time.time()
                time_i_j+=end-start
            time_i_j /= repeat_time
            time_i.append(time_i_j)
            con.commit()
            con.close()
        times.append(time_i)
    output_file = cur_path+"/../Result/TPCH/QueryTimeTPCH.txt"
    results = open(output_file, 'w')
    for i in range(len(S)):
        for j in range(len(Q)):
            results.write(S[i]+" Q"+str(Q[j])+" "+str(times[i][j])+"\n")
    
    
    
if __name__ == "__main__":
	main(sys.argv[1:])
    

