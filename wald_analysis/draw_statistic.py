#!/usr/bin/python3
import matplotlib.pyplot as plt
import numpy as np
import argparse

def get_params():
    parser = argparse.ArgumentParser(description='Convert stat-file to png.')
    parser.add_argument('stat_file',help='stat_file to convert',type=open)
    parser.add_argument('-o', '--outfile',help='Out png-file',type=str)
    return  parser.parse_args()

def stat2fig(stat_file,fig_file=None):
    if fig_file is None:
        fig_file = stat_file.replace('stat','png')
    plt.style.use('seaborn-notebook')
    f = open(stat_file)
    head_line = f.readline()
    f.close()
    head_list = head_line[1:].strip().split(',')
    statistic_data = np.loadtxt(stat_file,dtype='int')
    M,N = 1,len(head_list)
    fig, axes = plt.subplots(nrows=M,ncols=N,figsize=(4*N,4*M))
    axes.resize(M,N)
    for j in range(N):
        hist = statistic_data[2:,j]
        mn,mx = statistic_data[:2,j]
        k = np.linspace(start=mn,stop=mx,num=hist.shape[0]+1,endpoint=True)
        axes[0,j].set_title(head_list[j],fontweight="bold",size=14)
        sh = np.sum(hist)
        axes[0,j].bar(
            left=0.5*(k[:hist.shape[0]]+k[1:]),
            height=hist/sh,
            width=.6*(k[1]-k[0]),
            align='center'
        )
        axes[0,j].grid(True)
    plt.savefig(fig_file)

def main():
    args = get_params()
    if args.outfile is None:
        stat2fig(args.stat_file.name)
    else:
        stat2fig(args.stat_file.name,args.outfile)

if __name__ == '__main__':
    main()
