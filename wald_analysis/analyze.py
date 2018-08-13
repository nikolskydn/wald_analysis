#!/usr/bin/python3
import argparse
import json
import numpy as np
import scipy.sparse as sp
from wald_analysis import historgam as wh
from wald_analysis import transform as wt
import csv
import re

def get_params():

    parser = argparse.ArgumentParser(description='Analize unknow data.')
    parser.add_argument('-n', '--normal', help='Normal statistic file', 
                        type=open)
    parser.add_argument('unknow', help='Unknow csv first features file', 
                        type=open)
    parser.add_argument('-p', '--patterns', nargs='+',
                        help='Pattern statistic files', type=open)
    parser.add_argument('-s','--script',help='Transform script',type=open)
    parser.add_argument('-w','--window',help='Sliding window size',type=int, 
                        default=3)
    parser.add_argument('-o', '--outfile',help='Outfile with analyzes', 
                        type=str)
    return  parser.parse_args()




def main():

    np.set_printoptions(precision=3, suppress=True, linewidth=150,
                        formatter={'float':lambda x: '%6.1f'%x})
    args = get_params()
    normal = np.loadtxt(args.normal,comments='#',dtype=np.dtype(int),skiprows=1)
    patterns_list = [ np.loadtxt(pattern.name,comments='#', 
                                dtype=np.dtype(int),skiprows=1)
                      for pattern in args.patterns ]
    unknow = np.loadtxt(args.unknow,delimiter=',',comments='#',
                        dtype=np.dtype(int),skiprows=1)

    with open(args.script.name,'r',encoding='utf-8') as fj:
        script = json.load(fj)

    first_features = wt.Features(window=args.window)
    first_features.data = unknow

    alpha=0.01
    beta=0.01
    A=(1-beta)/alpha
    B=beta/(1-alpha)
    trans=wt.Transformer(script)
    second_features = np.array([trans(elem) for elem in first_features])

    anomalies = sp.lil_matrix((len(patterns_list),unknow.shape[0]))
    for pidx,pattern in enumerate(patterns_list):
        lh_functor = wh.LikelihoodRatio(normal_array=normal,
                                        pattern_array=pattern)
        lhs_buffer = []
        curr_anomalies = sp.lil_matrix((len(patterns_list),unknow.shape[0]))
        for idx,sfrow in enumerate(second_features):
            lhr = lh_functor(sfrow)
            if lhr > 1: 
                lhs_buffer.append(lhr)
            Lh = np.prod(np.array(lhs_buffer))
            if Lh >= A:
                curr_anomalies[pidx,idx:idx+first_features.window] = Lh
                mask = curr_anomalies>anomalies
                anomalies[mask] = curr_anomalies[mask]
                lhs_buffer.clear()
    result = anomalies.A
    full_patterns = args.patterns
    #full_patterns.insert(0,args.normal)
    with open(args.unknow.name,'r',newline='\n') as ufile:
        out_header = ufile.readline().rstrip().split(',')
    out_header.append('Pattern')
    if args.outfile is None:
        out_file_name = args.unknow.name.replace('.csv','-analyzed.csv')
    else:
        out_file_name = args.outfile
    with open(out_file_name,'w',newline='\n') as outfile:
        writer = csv.writer(outfile, delimiter=',')
        writer.writerow(out_header)
        for i in range(unknow.shape[0]):
            data_row = [ d for d in unknow[i] ]
            info = []
            sumlh = np.sum(result[:,i]) + 1e-15
            for j in range(result.shape[0]):
                prob = result[j][i]/sumlh
                if prob>1e-6:
                    pname = full_patterns[j].name.replace('.stat','')
                    info.append('{}:{:4.2f}'.format(pname,prob))
            if not info:
                data_row.append('normal')
            else:
                data_row.append('['+';'.join(info)+']')
            #
            writer.writerow(data_row)


if __name__=="__main__":
    main()
