import matplotlib.pyplot as plt
from random import random, seed
from math import tanh
import struct as st

seed(1)

#s=0
#r = [s:=(s+random()-.5) for _ in range(200)]
R = 100000
with open('Desktop/GRC-V0.11/prix/prixs.bin', 'rb') as co:
    t = co.read()
    R = st.unpack('I', t[:st.calcsize('I')])[0]
    t = t[st.calcsize('I'):]
    prixs = st.unpack(f'{R}f', t)

r = prixs[:300]

#plt.plot(r); plt.show()
#exit()

def ema(n):
    e = [r[0]]
    k = 1/(1+n)
    for i in range(1, len(r)):
        e += [e[-1]*(1-k) + r[i]*k]
    return e

ema2 = ema(3)
ema10 = ema(15)

def plot(*arr_t):
    for arr, t in arr_t:
        plt.plot(arr, label=t)
    plt.legend()
    plt.show()

from filtres import  *

K = 2
N = 7
w = [random()-.5 for _ in range(N)]

filtre0 = [random() for _ in range(2*K+1)]
filtre1 = [random() for _ in range(2*K+1)]
filtre2 = [random() for _ in range(2*K+1)]
filtre3 = [random() for _ in range(2*K+1)]
filtre4 = [random() for _ in range(2*K+1)]
filtre5 = [random() for _ in range(2*K+1)]

#plt.plot(filtre0);plt.plot(filtre1);plt.plot(filtre2);plt.show()

def mdl(w, _plot=False):
    global filtre0, filtre1, filtre2
    filtres0 = [0]*(2*K+1) + [filtrer(ema2, x-2*K-1, filtre0) for x in range(2*K+1,len(r))]
    filtres1 = [0]*(2*K+1) + [filtrer(ema2, x-2*K-1, filtre1) for x in range(2*K+1,len(r))]
    filtres2 = [0]*(2*K+1) + [filtrer(ema2, x-2*K-1, filtre2) for x in range(2*K+1,len(r))]
    filtres3 = [0]*(2*K+1) + [filtrer(ema2, x-2*K-1, filtre3) for x in range(2*K+1,len(r))]
    filtres4 = [0]*(2*K+1) + [filtrer(ema10, x-2*K-1, filtre4) for x in range(2*K+1,len(r))]
    filtres5 = [0]*(2*K+1) + [filtrer(ema10, x-2*K-1, filtre5) for x in range(2*K+1,len(r))]
    #
    DEPART = 100
    g = DEPART
    ___plt = [0]
    for i in range(len(r)-1):
        f = tanh(w[0]*filtres0[i] + w[1]*filtres1[i] + w[2]*filtres2[i] + w[3]*filtres3[i] + w[4]*filtres4[i] + w[5]*filtres5[i] + w[6])
        g += g*f*(r[i+1]/r[i]-1) * 100
        if _plot: ___plt += [g-DEPART]#[g-DEPART]
    if _plot: _min, _max = min(___plt), max(___plt); plt.plot([min(r)]*10+[(e-_min)/(_max-_min)/20 + min(r) for e in ___plt[10:]]); plt.plot(r);plt.show()
    return g - DEPART

def grad(w):
    _f = mdl(w)
    _grad = []
    for i in range(N):
        w[i] += 1e-5
        _grad += [(mdl(w)-_f)/1e-5]
        w[i] -= 1e-5
    return _grad

def dwidwi(w):
    _f = mdl(w)
    _grad = []
    for i in range(N):
        w[i] += 1e-5
        _fx = mdl(w)
        w[i] += 1e-5
        _grad += [(mdl(w)-2*_fx+_f)/1e-10]
        w[i] -= 2 * 1e-5
    return _grad

if __name__ == "__main__":
    #
    filtre = [0.0, 0.1, 0.3, 0.2, 0.7, 0.8, 0.9]
    K = (len(filtre)-1)//2
    #
    #plot((r, 'r'), (ema2, 'ema2'), (ema10, 'ema10'), (filtre, 'filtre'), (filtres, 'filtres'), (filtres_ema, 'filtres_ema'))
    print(mdl(w, _plot=True))
    print(w)
    for _ in range(10):
        g = grad(w)
        g2 = dwidwi(w)
        if sum(map(abs, g2))==0: continue
        alpha = 1 / sum(map(abs, dwidwi(w)))
        for i in range(N): w[i] += g[i]*alpha
    print(w)
    r = prixs[-300:]
    print(mdl(w, _plot=True))
