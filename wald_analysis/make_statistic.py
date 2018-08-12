#!/usr/bin/python3
import numpy as np
import argparse
import json
from wald_analysis import historgam as ht
from wald_analysis import transform as tf

def get_params():
    parser = argparse.ArgumentParser(description="Make netflow data statistics")
    parser.add_argument('from_csv',help="Input csv file",type=open)
    parser.add_argument('-t','--to_stat',help="Output statstic file",type=str)
    parser.add_argument('-s','--script',help="Transform script",type=open)
    parser.add_argument('-w','--window',help="Window for Feature",type=int, 
                        default=3)
    return parser.parse_args()


def main():

    args=get_params()

    with open(args.from_csv.name,'r',encoding='utf-8') as fc:
        fhead = fc.readline().strip().split(',')
        print(fhead)

    ff = tf.Features(window=args.window)
    ff.data = np.loadtxt(args.from_csv.name, dtype=np.dtype(int),
                       delimiter=',', skiprows=1)

    with open(args.script.name,'r',encoding='utf-8') as fj:
        script = json.load(fj)

    smaker = ht.MakeStatistic(trans=tf.Transformer(script))
    stats = smaker(ff)
    if args.to_stat is None:
        stat_name = args.from_csv.name.replace('.csv','.stat')
    else:
        stat_name  = args.to_stat
    np.savetxt(fname=stat_name, fmt='%7i', X=stats, 
               header=','.join(fhead[:len(fhead)-1]))

if __name__=="__main__":
    main()
