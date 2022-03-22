# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import sys
import os



def ReadData1(path):
    res = []
    errs = []
    times = []
    input_file = open(path, 'r')
    for line in input_file.readlines():
        elements = line.split()
        res.append(float(elements[1]))
        errs.append(float(elements[2]))
        times.append(float(elements[3]))
    return res,errs, times



def ReadData2(path):
    times = []
    input_file = open(path, 'r')
    for j in range(10):
        times.append([])
    lines = input_file.readlines()
    for i in range(7):
        for j in range(10):
            line = lines[i*10+j]
            elements = line.split()
            times[j].append(float(elements[2]))
    return times



def main(argv):
    Q = ["3","12","20"]
    res_q = []
    err_R2T = []
    err_LS = []
    time_R2T = []
    time_LS = []
    time_SQL = []
    time_extract = []
    cur_path=os.getcwd()

    for i in range(3):
        path = cur_path+"/../Result/TPCH/R2T_Q"+Q[i]+"_Scalability.txt"
        res,errs, times = ReadData1(path)
        res_q.append(res)
        err_R2T.append(errs)
        time_R2T.append(times)    
        path = cur_path+"/../Result/TPCH/LS_Q"+Q[i]+"_Scalability.txt"
        res,errs, times = ReadData1(path)
        err_LS.append(errs)
        time_LS.append(times)
    
    path = cur_path+"/../Result/TPCH/QueryTimeTPCH.txt"
    time_SQL = ReadData2(path)
    path = cur_path+"/../Result/TPCH/ExtractInfoTimeTPCH.txt"
    time_extract = ReadData2(path)
    
    for i in range(3):
        for j in range(7):
            time_R2T[i][j]+=time_extract[3+i][j]
            time_LS[i][j]+=time_extract[3+i][j]
    x=[0.125,0.25,0.5,1,2,4,8]
    fig, axes = plt.subplots(2,3, figsize=(24, 5.6))
    
    axes[0][0].tick_params(axis='both', which='major', labelsize=15)
    axes[0][0].axhline(y=10000000,ls="-",c=plt.cm.tab20c(19))
    axes[0][0].axhline(y=1000000,ls="-",c=plt.cm.tab20c(19))
    axes[0][0].axhline(y=100000,ls="-",c=plt.cm.tab20c(19))
    axes[0][0].axhline(y=10000,ls="-",c=plt.cm.tab20c(19))
    axes[0][0].set_facecolor("white")
    axes[0][0].plot(x, err_R2T[0],linewidth = 2.5, linestyle = '-.',label='R2T',
        marker = 's',markersize = 8,color=plt.cm.tab20c(0),
        markeredgecolor=plt.cm.tab20c(0),markeredgewidth = 1,markerfacecolor=plt.cm.tab20c(0))
    axes[0][0].plot(x, err_LS[0],linewidth = 2.5, linestyle = '--',label='LS',
        marker = 'v',markersize = 8,color=plt.cm.tab20c(6),
        markeredgecolor=plt.cm.tab20c(6),markeredgewidth = 2,markerfacecolor=plt.cm.tab20c(6))
    axes[0][0].plot(x, res_q[0],linewidth = 2.5,linestyle = ':',label='Query result',
        marker = 'o',markersize = 8,color=plt.cm.tab20c(9),
        markeredgecolor=plt.cm.tab20c(9),markeredgewidth = 1,markerfacecolor=plt.cm.tab20c(9))
    axes[0][0].set_yscale('log')
    axes[0][0].set_xscale('log')
    axes[0][0].set_title('$\mathregular{Q_{3}}$',fontsize=18)
    axes[0][0].set_ylabel("Error Level",fontsize=18)
    axes[0][0].legend(bbox_to_anchor=(-0.01, 0.5, 1, 1),fontsize=19,ncol=3, facecolor="white")
    
    axes[0][1].tick_params(axis='both', which='major', labelsize=15)
    axes[0][1].set_facecolor("white")
    axes[0][1].axhline(y=10000000,ls="-",c=plt.cm.tab20c(19))
    axes[0][1].axhline(y=1000000,ls="-",c=plt.cm.tab20c(19))
    axes[0][1].axhline(y=100000,ls="-",c=plt.cm.tab20c(19))
    axes[0][1].axhline(y=10000,ls="-",c=plt.cm.tab20c(19))
    axes[0][1].axhline(y=1000,ls="-",c=plt.cm.tab20c(19))
    axes[0][1].plot(x, err_R2T[1],linewidth = 2.5, linestyle = '-.',label='R2T',
        marker = 's',markersize = 8,color=plt.cm.tab20c(0),
        markeredgecolor=plt.cm.tab20c(0),markeredgewidth = 1,markerfacecolor=plt.cm.tab20c(0))
    axes[0][1].plot(x, err_LS[1],linewidth = 2.5, linestyle = '--',label='LS',
        marker = 'v',markersize = 8,color=plt.cm.tab20c(6),
        markeredgecolor=plt.cm.tab20c(6),markeredgewidth = 2,markerfacecolor=plt.cm.tab20c(6))
    axes[0][1].plot(x, res_q[1],linewidth = 2.5,linestyle = ':',label='Query result',
        marker = 'o',markersize = 8,color=plt.cm.tab20c(9),
        markeredgecolor=plt.cm.tab20c(9),markeredgewidth = 1,markerfacecolor=plt.cm.tab20c(9))
    axes[0][1].set_yscale('log')
    axes[0][1].set_xscale('log')
    axes[0][1].set_title('$\mathregular{Q_{12}}$',fontsize=18)
    
    axes[0][2].tick_params(axis='both', which='major', labelsize=15)
    axes[0][2].set_facecolor("white")
    axes[0][2].axhline(y=10000000,ls="-",c=plt.cm.tab20c(19))
    axes[0][2].axhline(y=1000000,ls="-",c=plt.cm.tab20c(19))
    axes[0][2].axhline(y=100000,ls="-",c=plt.cm.tab20c(19))
    axes[0][2].plot(x, err_R2T[2],linewidth = 2.5, linestyle = '-.',label='R2T',
        marker = 's',markersize = 8,color=plt.cm.tab20c(0),
        markeredgecolor=plt.cm.tab20c(0),markeredgewidth = 1,markerfacecolor=plt.cm.tab20c(0))
    axes[0][2].plot(x, err_LS[2],linewidth = 2.5, linestyle = '--',label='LS',
        marker = 'v',markersize = 8,color=plt.cm.tab20c(6),
        markeredgecolor=plt.cm.tab20c(6),markeredgewidth = 2,markerfacecolor=plt.cm.tab20c(6))
    axes[0][2].plot(x, res_q[2],linewidth = 2.5,linestyle = ':',label='Query result',
        marker = 'o',markersize = 8,color=plt.cm.tab20c(9),
        markeredgecolor=plt.cm.tab20c(9),markeredgewidth = 1,markerfacecolor=plt.cm.tab20c(9))
    axes[0][2].set_yscale('log')
    axes[0][2].set_xscale('log')
    axes[0][2].set_title('$\mathregular{Q_{20}}$',fontsize=18)
    
    axes[1][0].tick_params(axis='both', which='major', labelsize=15)
    axes[1][0].set_facecolor("white")
    axes[1][0].axhline(y=100,ls="-",c=plt.cm.tab20c(19))
    axes[1][0].axhline(y=10,ls="-",c=plt.cm.tab20c(19))
    axes[1][0].axhline(y=1,ls="-",c=plt.cm.tab20c(19))
    axes[1][0].plot(x, time_R2T[1],linewidth = 2.5, linestyle = '-.',label='R2T',
        marker = 's',markersize = 8,color=plt.cm.tab20c(0),
        markeredgecolor=plt.cm.tab20c(0),markeredgewidth = 1,markerfacecolor=plt.cm.tab20c(0))
    axes[1][0].plot(x, time_LS[1],linewidth = 2.5, linestyle = '--',label='LS',
        marker = 'v',markersize = 8,color=plt.cm.tab20c(6),
        markeredgecolor=plt.cm.tab20c(6),markeredgewidth = 2,markerfacecolor=plt.cm.tab20c(6))
    axes[1][0].plot(x, time_SQL[1],linewidth = 2.5,linestyle = ':',label='Query result',
        marker = 'o',markersize = 8,color=plt.cm.tab20c(9),
        markeredgecolor=plt.cm.tab20c(9),markeredgewidth = 1,markerfacecolor=plt.cm.tab20c(9))
    axes[1][0].set_yscale('log')
    axes[1][0].set_xscale('log')
    axes[1][0].set_ylabel("Running Time(s)",fontsize=18)
    axes[1][0].set_xlabel("Scale",fontsize=18)
    
    axes[1][1].tick_params(axis='both', which='major', labelsize=15)
    axes[1][1].set_facecolor("white")
    axes[1][1].axhline(y=100,ls="-",c=plt.cm.tab20c(19))
    axes[1][1].axhline(y=10,ls="-",c=plt.cm.tab20c(19))
    axes[1][1].axhline(y=1,ls="-",c=plt.cm.tab20c(19))
    axes[1][1].plot(x, time_R2T[1],linewidth = 2.5, linestyle = '-.',label='R2T',
        marker = 's',markersize = 8,color=plt.cm.tab20c(0),
        markeredgecolor=plt.cm.tab20c(0),markeredgewidth = 1,markerfacecolor=plt.cm.tab20c(0))
    axes[1][1].plot(x, time_LS[1],linewidth = 2.5, linestyle = '--',label='LS',
        marker = 'v',markersize = 8,color=plt.cm.tab20c(6),
        markeredgecolor=plt.cm.tab20c(6),markeredgewidth = 2,markerfacecolor=plt.cm.tab20c(6))
    axes[1][1].plot(x, time_SQL[1],linewidth = 2.5,linestyle = ':',label='Query result',
        marker = 'o',markersize = 8,color=plt.cm.tab20c(9),
        markeredgecolor=plt.cm.tab20c(9),markeredgewidth = 1,markerfacecolor=plt.cm.tab20c(9))
    axes[1][1].set_yscale('log')
    axes[1][1].set_xscale('log')
    axes[1][1].set_xlabel("Scale",fontsize=18)
    
    axes[1][2].tick_params(axis='both', which='major', labelsize=15)
    axes[1][2].set_facecolor("white")
    axes[1][2].axhline(y=100,ls="-",c=plt.cm.tab20c(19))
    axes[1][2].axhline(y=10,ls="-",c=plt.cm.tab20c(19))
    axes[1][2].axhline(y=1,ls="-",c=plt.cm.tab20c(19))
    axes[1][2].plot(x, time_R2T[2],linewidth = 2.5, linestyle = '-.',label='R2T',
        marker = 's',markersize = 8,color=plt.cm.tab20c(0),
        markeredgecolor=plt.cm.tab20c(0),markeredgewidth = 1,markerfacecolor=plt.cm.tab20c(0))
    axes[1][2].plot(x, time_LS[2],linewidth = 2.5, linestyle = '--',label='LS',
        marker = 'v',markersize = 8,color=plt.cm.tab20c(6),
        markeredgecolor=plt.cm.tab20c(6),markeredgewidth = 2,markerfacecolor=plt.cm.tab20c(6))
    axes[1][2].plot(x, time_SQL[2],linewidth = 2.5,linestyle = ':',label='Query result',
        marker = 'o',markersize = 8,color=plt.cm.tab20c(9),
        markeredgecolor=plt.cm.tab20c(9),markeredgewidth = 1,markerfacecolor=plt.cm.tab20c(9))
    axes[1][2].set_yscale('log')
    axes[1][2].set_xscale('log')
    axes[1][2].set_xticklabels(x)
    axes[1][2].set_xlabel("Scale",fontsize=18)  
    plt.savefig(cur_path+"/../Figure/Scalability.pdf")        

            

if __name__ == "__main__":
	main(sys.argv[1:])