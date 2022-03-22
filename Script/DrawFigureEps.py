# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import sys
import os



def ReadData(path):
    res = 0
    err = []
    input_file = open(path, 'r')
    for line in input_file.readlines():
        elements = line.split()
        res = float(elements[1])
        err.append(float(elements[2]))
    return res,err
        
        

def main(argv):
    Q = ["one_path","two_path","triangle", "rectangle"]
    M = ["R2T","LP","RM", "NT", "SDE"]
    err = []
    res = []
    cur_path=os.getcwd()
    for i in range(len(Q)):
        err_i = []
        res_i = 0
        for j in range(len(M)):
            if j==2:
                if i<2:
                    err_i.append([])
                    continue
            path = cur_path+"/../Result/Graph/"+M[j]+"_"+Q[i]+"_RoadnetPA.txt"
            res_i,err_ij = ReadData(path)
            err_i.append(err_ij)
        res.append(res_i)
        err.append(err_i)
    
    x=[0.1,0.2,0.4,0.8,1.6,3.2,6.4,12.8]
    fig, axes = plt.subplots(1,4, figsize=(36, 5))
    
    axes[0].tick_params(axis='both', which='major', labelsize=15)
    axes[0].set_facecolor("white")
    axes[0].axhline(y=res[0],ls="--",c='black',alpha=0.6,label='Query result')
    axes[0].plot(x, err[0][0],linewidth = 2.5, linestyle = '-.',label='R2T',
        marker = 's',markersize = 8,color=plt.cm.tab20c(0),
        markeredgecolor=plt.cm.tab20c(0),markeredgewidth = 1,markerfacecolor=plt.cm.tab20c(0))
    axes[0].plot(x, err[0][1],linewidth = 2.5,linestyle = '-.',label='LP',
        marker = 's',markersize = 8,color=plt.cm.tab20c(12),
        markeredgecolor=plt.cm.tab20c(12),markeredgewidth = 2,markerfacecolor='w')
    axes[0].plot(x, err[0][3],linewidth = 2.5, linestyle = '--',label='NT',
        marker = 'v',markersize = 8,color=plt.cm.tab20c(6),
        markeredgecolor=plt.cm.tab20c(6),markeredgewidth = 2,markerfacecolor=plt.cm.tab20c(6))
    axes[0].plot(x, err[0][4],linewidth = 2.5,linestyle = '--',label='SDE',
        marker = 'v',markersize = 8,color=plt.cm.tab20b(8),
        markeredgecolor=plt.cm.tab20b(8),markeredgewidth = 2,markerfacecolor='w')
    axes[0].set_yscale('log')
    axes[0].set_xscale('log')
    axes[0].set_title('Edge counting',fontsize=23)
    axes[0].set_ylabel("Error Level",fontsize=23)
    axes[0].set_xlabel(r"value of $\epsilon$",fontsize=23)
    
    axes[1].tick_params(axis='both', which='major', labelsize=15)
    axes[1].set_facecolor("white")
    axes[1].axhline(y=res[1],ls="--",c='black',alpha=0.6,label='Query result')
    axes[1].plot(x, err[1][0],linewidth = 2.5, linestyle = '-.',label='R2T',
        marker = 's',markersize = 8,color=plt.cm.tab20c(0),
        markeredgecolor=plt.cm.tab20c(0),markeredgewidth = 1,markerfacecolor=plt.cm.tab20c(0))
    axes[1].plot(x, err[1][1],linewidth = 2.5,linestyle = '-.',label='LP',
        marker = 's',markersize = 8,color=plt.cm.tab20c(12),
        markeredgecolor=plt.cm.tab20c(12),markeredgewidth = 2,markerfacecolor='w')
    axes[1].plot(x, err[1][3],linewidth = 2.5, linestyle = '--',label='NT',
        marker = 'v',markersize = 8,color=plt.cm.tab20c(6),
        markeredgecolor=plt.cm.tab20c(6),markeredgewidth = 2,markerfacecolor=plt.cm.tab20c(6))
    axes[1].plot(x, err[1][4],linewidth = 2.5,linestyle = '--',label='SDE',
        marker = 'v',markersize = 8,color=plt.cm.tab20b(8),
        markeredgecolor=plt.cm.tab20b(8),markeredgewidth = 2,markerfacecolor='w')
    axes[1].set_yscale('log')
    axes[1].set_xscale('log')
    axes[1].set_title('Length-2 path counting',fontsize=23)
    axes[1].set_xlabel(r"value of $\epsilon$",fontsize=23)
    
    axes[2].tick_params(axis='both', which='major', labelsize=15)
    axes[2].set_facecolor("white")
    axes[2].axhline(y=res[2],ls="--",c='black',alpha=0.6,label='Query result')
    axes[2].plot(x, err[2][1],linewidth = 2.5,linestyle = '-.',label='LP',
        marker = 's',markersize = 8,color=plt.cm.tab20c(12),
        markeredgecolor=plt.cm.tab20c(12),markeredgewidth = 2,markerfacecolor='w')
    axes[2].plot(x, err[2][2],linewidth = 2.5,linestyle = ':',label='Rec',
        marker = 'o',markersize = 8,color=plt.cm.tab20c(9),
        markeredgecolor=plt.cm.tab20c(9),markeredgewidth = 1,markerfacecolor=plt.cm.tab20c(9))
    axes[2].plot(x, err[2][3],linewidth = 2.5, linestyle = '--',label='NT',
        marker = 'v',markersize = 8,color=plt.cm.tab20c(6),
        markeredgecolor=plt.cm.tab20c(6),markeredgewidth = 2,markerfacecolor=plt.cm.tab20c(6))
    axes[2].plot(x, err[2][4],linewidth = 2.5,linestyle = '--',label='SDE',
        marker = 'v',markersize = 8,color=plt.cm.tab20b(8),
        markeredgecolor=plt.cm.tab20b(8),markeredgewidth = 2,markerfacecolor='w')
    axes[2].plot(x, err[2][0],linewidth = 2.5, linestyle = '-.',label='R2T',
        marker = 's',markersize = 8,color=plt.cm.tab20c(0),
        markeredgecolor=plt.cm.tab20c(0),markeredgewidth = 1,markerfacecolor=plt.cm.tab20c(0))
    axes[2].set_yscale('log')
    axes[2].set_xscale('log')
    axes[2].set_title('Triangle counting',fontsize=23)
    axes[2].set_xlabel(r"value of $\epsilon$",fontsize=23)

    axes[3].tick_params(axis='both', which='major', labelsize=15)
    axes[3].set_facecolor("white")
    axes[3].axhline(y=res[3],ls="--",c='black',alpha=0.6,label='Query result')
    axes[3].plot(x, err[3][1],linewidth = 2.5,linestyle = '-.',label='LP',
        marker = 's',markersize = 8,color=plt.cm.tab20c(12),
        markeredgecolor=plt.cm.tab20c(12),markeredgewidth = 2,markerfacecolor='w')
    axes[3].plot(x, err[3][2],linewidth = 2.5,linestyle = ':',label='Rec',
        marker = 'o',markersize = 8,color=plt.cm.tab20c(9),
        markeredgecolor=plt.cm.tab20c(9),markeredgewidth = 1,markerfacecolor=plt.cm.tab20c(9))
    axes[3].plot(x, err[3][3],linewidth = 2.5, linestyle = '--',label='NT',
        marker = 'v',markersize = 8,color=plt.cm.tab20c(6),
        markeredgecolor=plt.cm.tab20c(6),markeredgewidth = 2,markerfacecolor=plt.cm.tab20c(6))
    axes[3].plot(x, err[3][4],linewidth = 2.5,linestyle = '--',label='SDE',
        marker = 'v',markersize = 8,color=plt.cm.tab20b(8),
        markeredgecolor=plt.cm.tab20b(8),markeredgewidth = 2,markerfacecolor='w')
    axes[3].plot(x, err[3][0],linewidth = 2.5, linestyle = '-.',label='R2T',
        marker = 's',markersize = 8,color=plt.cm.tab20c(0),
        markeredgecolor=plt.cm.tab20c(0),markeredgewidth = 1,markerfacecolor=plt.cm.tab20c(0))
    axes[3].set_yscale('log')
    axes[3].set_xscale('log')
    axes[3].set_title('Rectangle counting',fontsize=23)
    axes[3].set_xlabel(r"value of $\epsilon$",fontsize=23)
    axes[3].legend(bbox_to_anchor=(-3.7, 0.46, 1, 1),fontsize=19,ncol=3, facecolor="white")
    plt.savefig(cur_path+"/../Figure/Eps.pdf")  

if __name__ == "__main__":
	main(sys.argv[1:])