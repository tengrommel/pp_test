# IPython log file

get_ipython().magic('logstart')
get_ipython().magic('logstart')
get_ipython().magic('logstop')
get_ipython().magic('logstart')
get_ipython().system('data')
get_ipython().system('date')
get_ipython().system('ls')
date = get_ipython().getoutput('date')
date
a=2+2
a
get_ipython().magic('hist')
get_ipython().system('history')
get_ipython().magic('hist -g a = 2')
get_ipython().magic('hist -g a = 2')
get_ipython().magic('hist -g a = 2')
a = arange(5)
import numpy as np
a = np.arange(5)
a.dtype
a.shape
m = np.array([arange(2), arange(2)])
m = np.array([np.arange(2), np.arange(2)])
m
m.shape
ab=np.array([1,2,3], [4,5,6])
ab=np.array([[1,2,3],[4,5]])
ab.shape
ab.shape[0]
ab
ab
ab[0,0]
a
a
a[0]
m[0]
ab[0]
ab[0,0]
