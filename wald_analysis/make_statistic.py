#!/usr/bin/python3
import numpy as np
import argparse
import json
from wald_analysis import historgam as wh
from wald_analysis import transform as wt

def get_params():
    parser = argparse.ArgumentParser(description= ('Make statistic file'+ 
                                                   'with histogramm'))
    parser.add_argument('from_csv',help='Input csv file',type=open)
    parser.add_argument('-t','--to_stat',help='Output statstic file',type=str)
    parser.add_argument('-s','--script',help='Transform script',type=open)
    parser.add_argument('-w','--window',help='Sliding window size',type=int, 
                        default=3)
    return parser.parse_args()


def main():

    args=get_params()
    if args.to_stat is None:
        stat_name = args.from_csv.name.replace('.csv','.stat')
    else:
        stat_name  = args.to_stat
    ff = wt.Features(window=args.window)
    ff.data = np.loadtxt(args.from_csv.name, dtype=np.dtype(int),
                       delimiter=',', skiprows=1)
    with open(args.script.name,'r',encoding='utf-8') as fj:
        script = json.load(fj)
    smaker = wh.MakeStatistic(trans=wt.Transformer(script))
    stats = smaker(ff)
    np.savetxt(fname=stat_name,fmt='%7i',X=stats,
               header=','.join(script['sfhead']))

if __name__=="__main__":
    main()
