from math import exp
import matplotlib.pyplot as plt

def filtrer(_r, x, filtre):
    a = _r[x:x+len(filtre)]
    _max, _min = max(a), min(a)
    a = [(e-_min)/(_max-_min) for e in a]
    #
    _s = sum( (1+abs(a[i] - filtre[i]))**2-1 for i in range(len(filtre)) ) / len(filtre)
    _c = exp(-_s**2)
    #
    _delta = sum(  (1+abs((a[i+1]-a[i])-(filtre[i+1]-filtre[i])))**2-1 for i in range(len(filtre)-1))/(len(filtre)-1)
    _delta = exp(-_delta**2)
    #
    return (_c*_delta)**.5
