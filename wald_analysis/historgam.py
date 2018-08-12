#!/usr/bin/python3
import numpy as np
#import pdb

class HistorgamMaker(object):
    """ Histogram creation functor.

    It is frequency distribution.

    """


    def __init__(self, intervals_number=30):
        self._intervals_number=intervals_number

    def __call__(self, features):
        """ Converts features to a histogram. """
        row_number, col_number = features.shape
        histogram = np.zeros((self._intervals_number+2,col_number), dtype=int)
        hist_min = np.min(features, axis=0)
        hist_max = np.max(features, axis=0)
        hist_half_step = 1./self._intervals_number
        hist_min = hist_min - hist_half_step
        hist_max = hist_max + hist_half_step
        histogram[0,:] = np.floor(hist_min)
        histogram[1,:] = np.ceil(hist_max)
        for j in range(col_number):
            ibins = np.linspace(start=histogram[0,j],
                                stop=histogram[1,j],
                                num=self._intervals_number+1,
                                endpoint=True)
            for i in range(self._intervals_number):
                if i == 0:
                    histogram[i+2,j] += np.sum(np.logical_and(
                                               features[:,j]>=ibins[i],
                                               features[:,j]<=ibins[i+1]))
                else:
                    histogram[i+2,j] += np.sum(np.logical_and(
                                               features[:,j]>ibins[i],
                                               features[:,j]<=ibins[i+1]))
        return histogram


class GetProbability(object):
    """ Return probobility  """

    def __init__(self, hist):
        self._hist=hist
        self.__mn, self.__mx = self._hist[:2]
        self.__data = self._hist[2:]
        self.__rows, self.__cols = self.__data.shape

    def __call__(self, values):

        row_idx = -np.ones(self.__cols,dtype=int)
        for j in range(self.__cols):
            ibins = np.linspace(start=self.__mn[j],stop=self.__mx[j],
                                num=self.__rows+1,endpoint=True)
            for i in range(self.__rows):
                if i == 0:
                    if values[j]>=ibins[i] and values[j]<=ibins[i+1]:
                        row_idx[j] = i
                else:
                    if values[j]>ibins[i] and values[j]<=ibins[i+1]:
                        row_idx[j] = i

        col_idx=np.arange(self.__cols)
        good_idx = np.logical_and(row_idx>=0,row_idx<=self.__rows-1)
        nm = np.sum(self.__data,axis=0)
        if np.all(good_idx):
            return self.__data[row_idx,col_idx] / nm
        else:
            return np.array([self.__data[row_idx[i],col_idx[i]] 
                              if good_idx[i] else 0.0  
                              for i in np.arange(self.__cols)]) / nm

class MakeStatistic(object):
    """ Converts the first features into a histogram.

    To transform first features into secondary ones, 
    the functor from the field strategy is used.

    An example

    ```from traffic_statistic import transform as tf```
    ```from traffic_statistic import historgam as ht```
    ```smaker = ht.MakeStatistic()```
    ```smaker.strategy = tf.LoadAmplification()```
    ```stats = smaker(first_features)``` 

    """

    def __init__(self,trans):
        self._hist = HistorgamMaker()
        self._trans = trans
        
    def __call__(self,first_features):
        return self._hist(np.array([self._trans(elem) 
                                    for elem in first_features]))

class LikelihoodRatio(object):
    """ Calculates likelihood ration. """

    def __init__(self,normal_array,pattern_array,alpha=0.05,delta=1e-15):
        self._normal = GetProbability(normal_array)
        self._pattern = GetProbability(pattern_array)
        self._delta = delta

    #normal = property
    #pattern = property
        
    def __call__(self,second_features_row):
            W0=np.prod(self._normal(second_features_row))
            WP=np.prod(self._pattern(second_features_row))
            return WP/(W0+self._delta)


if __name__=="__main__":

    np.set_printoptions(precision=2, suppress=True, linewidth=150,
                        formatter={'float':lambda x: '%10.2f'%x})

    hist = HistorgamMaker(5)
    test_data = np.array([
        [1,1,0,0],
        [0,2,0,0],
        [0,0,1,0],
        [0,0,0,1]
    ])
    stats = hist(test_data)
    print(stats)
    get=GetProbability(stats)
    print('get(np.array([0.95,2.0,0.1,0.1]))')
    print(get(np.array([0.95,2.0,0.1,0.1])))
    print('get(np.array([0.95+1,1.99,0.0,0.1-10]))')
    print(get(np.array([0.95+1,1.99,0.0,0.1-10])))
