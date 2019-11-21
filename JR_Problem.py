# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 03:12:40 2019
@author: nowshad
"""
import pandas as pd
import numpy as np
import csv 

def Find_seq(DataSet):
    l=DataSet.shape[0]
    seq=[]
    for i in range(l):
        seq.insert(i,0)
    i,j=0,l-1
    while DataSet.empty==False:
        M1_min=DataSet['M1'].min()
        M2_min=DataSet['M2'].min()
        if M1_min>M2_min:
            index=DataSet['M2'].idxmin()
            job=DataSet['Job'][index]
            seq[j]=job
            j-=1
            DataSet = DataSet.drop([index], axis=0)
        else:
            index=DataSet['M1'].idxmin()
            job=DataSet['Job'][index]
            seq[i]=job
            i+=1
            DataSet = DataSet.drop([index], axis=0)
    return seq
    
def FindInOut_Table(DataSet,seq):
    InOut={'JobSeq':['M1_in','M1_out','M2_in','M2_out']}
    for i in range(DataSet.shape[0]):
        if i==0:
            idx = DataSet[DataSet['Job']==seq[i]].index.values.astype(int)
            InOut[seq[i]]=[0,DataSet['M1'][idx[0]],DataSet['M1'][idx[0]],DataSet['M1'][idx[0]]+DataSet['M2'][idx[0]]]
        else:
            idx = DataSet[DataSet['Job']==seq[i]].index.values.astype(int)
            M1outTemp=InOut[seq[i-1]][1]+DataSet['M1'][idx[0]];
            if M1outTemp>InOut[seq[i-1]][3]:
                M2inTemp=M1outTemp
            else:
                M2inTemp=InOut[seq[i-1]][3]
            InOut[seq[i]]=[InOut[seq[i-1]][1],M1outTemp,M2inTemp,M2inTemp+DataSet['M2'][idx[0]]]
    
    InOutTable=pd.DataFrame.from_dict(InOut, orient='index')    
    return InOutTable
    
def Calculate_FlowAndIdleTime(InOutTable):
    print("\nTotal Flow Time: ",InOutTable[3][InOutTable.shape[0]-1])
    M1_IdleTime=InOutTable[3][InOutTable.shape[0]-1]-InOutTable[1][InOutTable.shape[0]-1]
    print("M1 Idle Time: ", M1_IdleTime)
    M2_IdleTime=0
    for i in range(InOutTable.shape[0]-1):
        if i==0:
            M2_IdleTime=InOutTable[2][1]-InOutTable[0][1]
            
        else:
            M2_IdleTime=M2_IdleTime+(InOutTable[2][i+1]-InOutTable[3][i])        
    print("M2 Idle Time: ", M2_IdleTime)
#Main
dataset = pd.read_csv('G:\AUST4.1\IPE\ASSgnmt\JR.csv')
print("\nSize:- ", dataset.shape) 
print("\n", dataset)
seq=Find_seq(dataset)
print("\nSequence: ",seq,"\n")
InOutTable=FindInOut_Table(dataset,seq)
print(InOutTable)
Calculate_FlowAndIdleTime(InOutTable)
