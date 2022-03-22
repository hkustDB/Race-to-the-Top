# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import sys
import os



def ReadData(path):
    err = []
    input_file = open(path, 'r')
    for line in input_file.readlines():
        elements = line.split()
        err.append(float(elements[1]))
    return err



def main(argv):
    Q = ["3","12","20"]
    Q_R = [2888656, 6001215, 6001215]
    err_R2T = []
    err_LS = []
    cur_path=os.getcwd()
    for i in range(3):
        path = cur_path+"/../Result/TPCH/R2T_Q"+Q[i]+"_GS.txt"
        err = ReadData(path)
        err_R2T.append(err)
        path = cur_path+"/../Result/TPCH/LS_Q"+Q[i]+"_GS.txt"
        err= ReadData(path)
        err_LS.append(err)
    GS = 10000
    x=[]
    for i in range(8):
        x.append(GS)
        GS*=10
    fig, axes = plt.subplots(1,3, figsize=(24, 2.6))
    
    axes[0].tick_params(axis='both', which='major', labelsize=15)
    axes[0].set_facecolor("white")
    axes[0].axhline(y=Q_R[0],ls="--",c='black',alpha=0.6,label='Query result')
    axes[0].plot(x, err_R2T[0],linewidth = 2.5, linestyle = '-.',label='R2T',
        marker = 's',markersize = 8,color=plt.cm.tab20c(0),
        markeredgecolor=plt.cm.tab20c(0),markeredgewidth = 1,markerfacecolor=plt.cm.tab20c(0))
    axes[0].plot(x, err_LS[0],linewidth = 2.5, linestyle = '--',label='LS',
        marker = 'v',markersize = 8,color=plt.cm.tab20c(6),
        markeredgecolor=plt.cm.tab20c(6),markeredgewidth = 2,markerfacecolor=plt.cm.tab20c(6))
    axes[0].set_yscale('log')
    axes[0].set_xscale('log')
    axes[0].set_title('$\mathregular{Q_{3}}$',fontsize=18)
    axes[0].set_ylabel("Error Level",fontsize=18)
    axes[0].legend(bbox_to_anchor=(-0.01, 0.5, 1, 1),fontsize=19,ncol=3, facecolor="white")
    axes[0].set_xlabel("$\mathregular{GS_Q}$",fontsize=18) 
    
    axes[1].tick_params(axis='both', which='major', labelsize=15)
    axes[1].set_facecolor("white")
    axes[1].axhline(y=Q_R[1],ls="--",c='black',alpha=0.6,label='Query result')
    axes[1].plot(x, err_R2T[1],linewidth = 2.5, linestyle = '-.',label='R2T',
        marker = 's',markersize = 8,color=plt.cm.tab20c(0),
        markeredgecolor=plt.cm.tab20c(0),markeredgewidth = 1,markerfacecolor=plt.cm.tab20c(0))
    axes[1].plot(x, err_LS[1],linewidth = 2.5, linestyle = '--',label='LS',
        marker = 'v',markersize = 8,color=plt.cm.tab20c(6),
        markeredgecolor=plt.cm.tab20c(6),markeredgewidth = 2,markerfacecolor=plt.cm.tab20c(6))
    axes[1].set_yscale('log')
    axes[1].set_xscale('log')
    axes[1].set_title('$\mathregular{Q_{12}}$',fontsize=18)
    axes[1].set_ylabel("Error Level",fontsize=18)
    axes[1].set_xlabel("$\mathregular{GS_Q}$",fontsize=18) 
    
    axes[2].tick_params(axis='both', which='major', labelsize=15)
    axes[2].set_facecolor("white")
    axes[2].axhline(y=Q_R[2],ls="--",c='black',alpha=0.6,label='Query result')
    axes[2].plot(x, err_R2T[2],linewidth = 2.5, linestyle = '-.',label='R2T',
        marker = 's',markersize = 8,color=plt.cm.tab20c(0),
        markeredgecolor=plt.cm.tab20c(0),markeredgewidth = 1,markerfacecolor=plt.cm.tab20c(0))
    axes[2].plot(x, err_LS[2],linewidth = 2.5, linestyle = '--',label='LS',
        marker = 'v',markersize = 8,color=plt.cm.tab20c(6),
        markeredgecolor=plt.cm.tab20c(6),markeredgewidth = 2,markerfacecolor=plt.cm.tab20c(6))
    
    axes[2].set_yscale('log')
    axes[2].set_xscale('log')
    axes[2].set_title('$\mathregular{Q_{20}}$',fontsize=18)
    axes[2].set_ylabel("Error Level",fontsize=18)
    axes[2].set_xlabel("$\mathregular{GS_Q}$",fontsize=18) 
    plt.savefig(cur_path+"/../Figure/GS.pdf")   
        
    
if __name__ == "__main__":
	main(sys.argv[1:])