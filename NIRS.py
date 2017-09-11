# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 16:59:13 2017

@author: okamoto
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



data = pd.read_csv("INPUTDATA.csv",header = 54,encoding="shift-jis")

def sampling(prerest):
    print('loading now...')
    Mark = []
    for i in range(0,len(data)-1):
        if data["Mark"][i] + data["Mark"][i+1] == 1:
            if data["Mark"][i] == 0:
                Mark.append(i-prerest+1)
            else:
                Mark.append(i+prerest)    
    return Mark

def block(Mk_l,sec,esec):
    oxy_lis = []
    for i in range(0,sec):
        a = []
        t = 0
        
        for l in range(0,esec):
            ll = int(i*4+l*2)
            a.append(data.iloc[Mk_l[ll]:Mk_l[ll+1],7:17].values)
            if t <= len(a[l]):
                t = len(a[l])
                   
        for k in range(0,esec):
            if t != len(a[k]):
                tt = int(t-len(a[k]))
                a_mean = np.reshape(a[k][-11:-1].mean(axis=0),[1,10])
                a_mean = np.resize(a_mean,[tt,10])
                a[k] = np.append(a[k],a_mean,axis=0)
                print(len(a[k]))
                
        a_total = np.zeros([t,10])
        
        for ll in range(0,esec):
            a_total += a[ll]
            
        a_total /= esec
        oxy_lis.append(a_total)
        
    return oxy_lis,a_mean

def fitting(prerest,Mk_l,sec):
    oxy_lis = []
    for i in range(0,sec):
        
        testx = np.arange(0,prerest)
        testx = np.append(testx,np.arange(len(Mk_l[i])-prerest,len(Mk_l[i])))
        testy = Mk_l[i][testx]
#    testx = np.resize(testx,[prerest*2,10]).T
        sji = np.polyfit(testx,testy,1)
        tempx = np.arange(0,len(Mk_l[i]))
        tempy = np.matrix(sji[0,:]).T*np.matrix(tempx)
        tempy = tempy.T
        tyy = Mk_l[i] - tempy
        oxy_lis.append(tyy)
    return oxy_lis
    

Mk = sampling(5)
ab,tt = block(Mk,5,2)
tyy = fitting(5,ab,5)
