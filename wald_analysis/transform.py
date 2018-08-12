#!/usr/bin/python3
import numpy as np

class Features(object):
    """ Container for storage of features.

    Used to iterate the features in a window.

    """


    def __init__(self, window=3):
        self._data = None
        self._counter = 0
        self._window = window
        self._rows = 0
        self._cols = 0

    def _data_get(self):
        return self._data

    def _data_set(self, array):
        self._rows,self._cols = array.shape
        self._data = array

    data = property(fget=_data_get, fset=_data_set)

    def _window_get(self):
        return self._window

    def _window_set(self, value):
        self._window = value

    window = property(fget=_window_get, fset=_window_set)

    def __iter__(self):
        self._counter = 0
        return self

    def __next__(self):
        idx=self._counter
        if idx < self._rows-self._window+1:
            self._counter += 1
            return self._data[idx:idx+self._window,:]
        else:
            raise StopIteration

def Median(data):
    return np.median(data,axis=0)

def Mean(data):
    return np.mean(data,axis=0)

def Divide(data):
    return data[:,0]/data[:,1]

class Transformer(object):
    """ Transform first features to second features. 

    """
  
 
    def __init__(self,scripts=[{'idxs':slice(None,None,1),
                                'ops':['Median']}]):
        self._scripts = scripts

    def __call__(self,data):
        stokes = []
        for script in self._scripts:
            cols = data[:,script['idxs']]
            for op in script['ops']:
                cols = eval(op)(cols)
            stokes.append(cols)
        return np.hstack(stokes)


if __name__=="__main__":

    np.set_printoptions(precision=2, suppress=True, linewidth=150,
                        formatter={'float':lambda x: '%10.2f'%x})
    ff=Features()
    ff.window=3

    my_scripts = [{'idxs':[0,1],'ops':['Median']},
                  {'idxs':[2],'ops':['Mean','np.square']},
                  {'idxs':[3,4],'ops':['Divide','Median']}]
    Tr=Transformer(my_scripts)
    ff.data = np.array([
        [1,4,2,3,1],
        [4,1,5,6,2],
        [7,0,8,4,2],
        [0,7,5,2,1],
    ])
    print(ff.data)
    print(np.array([Tr(elem) for elem in ff]))

