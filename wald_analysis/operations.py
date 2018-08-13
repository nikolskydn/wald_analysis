#!/usr/bin/python3
import numpy as np

class Median(object):

    def __call__(self,data):
        return np.median(data,axis=0)


class Mean(object):

    def __call__(self,data):
        return np.mean(data,axis=0)


class Divide(object):

    def __call__(self,data):
        return data[:,0]/data[:,1]


class Number(object):

    def __init__(self,check_values_list):
        self._check_values_list = check_values_list

    def __call__(self,data):
        result = -1.*np.ones_like(data)
        for idx,val in enumerate(self._check_values_list):
            result[data==val] = idx
        return result

#def NumberNetFlowPort(data):
#    return Number(data,check_values_list=[0,53,123,1900])

if __name__=="__main__":

    np.set_printoptions(precision=2, suppress=True, linewidth=150,
                        formatter={'float':lambda x: '%10.2f'%x})

    data = np.array([[1,2,3],[1,5,6],[0,53,123]])

    print("\033[33;1mInput data\033[0m")
    print(data)

    functs1 = [ Median(), Mean(), Number([0,53,123]) ]

    for funct in functs1:
        print('\033[33;1m{:10s}: \033[0m{}'.format(funct.__class__.__name__,
                                                   funct(data)))

    print('\033[33;1m{:10s}: \033[0m{}'.format('Divide(c0/c1)',
                                               Divide()(data[:,:2])))
