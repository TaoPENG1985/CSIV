from cmath import nan
from random import random
from tarfile import NUL
from types import resolve_bases
import numpy as np
from sklearn.metrics import mean_squared_error
import math 
from scipy import stats
import os
import time
import pandas as pd
from sklearn.preprocessing import scale
import matplotlib.pyplot as plt
import numpy as np 


sizeWin  = 10000
indexRatiMV  = 0
star = 0.5
fin = 0.6
# dataSet = "A" 
dataSet = "C" 

# MV_ou_nonMV = "imputed values"
# MV_ou_nonMV = "non-missing values"


'''
第一步读取相应的文件
'''
if(dataSet == "C"):
    nomFile = ['ISTM_resultat/CityPulse/ISTM_OPM_E_repare_et_E_original_all_BackTime6_modelTestNon5.npy',
                'ISTM_resultat/CityPulse/ISTM_OPM_E_repare_et_E_original_all_BackTime6_modelTestNon10.npy',
                'ISTM_resultat/CityPulse/ISTM_OPM_E_repare_et_E_original_all_BackTime6_modelTestNon15.npy',
                'ISTM_resultat/CityPulse/ISTM_OPM_E_repare_et_E_original_all_BackTime6_modelTestNon20.npy',
                'ISTM_resultat/CityPulse/ISTM_OPM_E_repare_et_E_original_all_BackTime6_modelTestNon25.npy']
    tousLesVoisinsDeTouslesPionts = 'ISTM_resultat/CityPulse/tousLesVoisinsDeTouslesPionts.npy'
elif(dataSet == "A"): 
    nomFile = ['ISTM_resultat/AEP/ISTM_OPM_E_repare_et_E_original_all_BackTime4_modelTestNon5.npy',
    'ISTM_resultat/AEP/ISTM_OPM_E_repare_et_E_original_all_BackTime4_modelTestNon10.npy',
    'ISTM_resultat/AEP/ISTM_OPM_E_repare_et_E_original_all_BackTime4_modelTestNon15.npy',
    'ISTM_resultat/AEP/ISTM_OPM_E_repare_et_E_original_all_BackTime4_modelTestNon20.npy',
    'ISTM_resultat/AEP/ISTM_OPM_E_repare_et_E_original_all_BackTime4_modelTestNon25.npy']
    tousLesVoisinsDeTouslesPionts = 'ISTM_resultat/AEP/tousLesVoisinsDeTouslesPionts_RH_TH.npy'


E_resultat, E_original, E_a_reparer,E_prediction = np.load(nomFile[indexRatiMV], allow_pickle=True)
# E_resultat 是 含有预测结果数据集，所有缺失值都已经被修复了
# E_original 是原始数据，含有原始缺失值（用-1表示）
# E_a_reparer 含有非缺失值， 含有原始缺失值（用-1表示），含有模拟缺失值（-2表示）
# E_prediction 含有全部的预测值，自然不含缺失值

VoisinsSensor = np.load(tousLesVoisinsDeTouslesPionts, allow_pickle=True)
indexNomeSensor = np.array ([x[0] for x in VoisinsSensor])

numVoisin = []
for i in VoisinsSensor:
    numVoisin.append(len(i))
print(" numVoisin mean", np.mean(numVoisin))
print(" numVoisin min", np.min(numVoisin))
print(" numVoisin ma x", np.max(numVoisin))

'''
确认窗口大小，开始位置（30%，之前的确认分布参数），结束位置就是最后一个
'''
numSensor, numIndex = E_resultat.shape
indexStar = int(numIndex*star)
indexFini = int(numIndex*fin-1)



for MV_ou_nonMV in ["imputed values", "non-missing values"]:
    for indexRatiMV  in [0,2,4]:
    # for indexRatiMV  in [4]:

        errNonMVList = []
        errSMVLsit =  []
        SMVLsit = []
        nonSMVList = []

        for  j in range(indexStar-sizeWin,indexStar):
            # for i in range(numSensor):
            for i in [7]:
                # if (E_original[i][j] < 60 and E_original[i][j] >20 ): #取特定区间
                if (True ): #
                    if (E_a_reparer[i][j]  == -2): #模拟缺失值
                        errSMVLsit.append(E_prediction[i][j] - E_original[i][j])
                        SMVLsit.append(E_prediction[i][j])
            
                    if(E_a_reparer[i][j] != -1 and E_a_reparer[i][j] != -2):
                        errNonMVList.append(E_prediction[i][j] - E_original[i][j])
                        nonSMVList.append(E_original[i][j])
            
        err_mean_SMV , std_mean_SMV = np.mean(errSMVLsit) , np.std(errSMVLsit)
        err_mean_nonMV , std_mean_nonMV = np.mean(errNonMVList) , np.std(errNonMVList)

        conf_interal_nonMV = stats.norm.interval(0.95, loc= err_mean_nonMV, scale = std_mean_nonMV)
        conf_interal_SMV = stats.norm.interval(0.95, loc= err_mean_SMV, scale = std_mean_SMV)

        # print ("errSMVLsit ",stats.kstest(errSMVLsit, 'norm'))  
        # print ("errSMVLsit asym ",stats.kstest(SMVLsit, 'norm',mode = 'asymp'))  

        # print ("nonSMVList asym ",stats.kstest(nonSMVList, 'norm',mode = 'asymp'))  
        print ("nonSMVList ",stats.kstest(nonSMVList, 'norm'))  
        # print ("SMVLsit asym ",stats.kstest(SMVLsit, 'norm',mode = 'asymp'))  
        print ("SMVLsit ",stats.kstest(SMVLsit, 'norm'))  



        plt.figure(figsize=(6,5.5))
        if MV_ou_nonMV == "imputed values":   
            plt.hist(SMVLsit,bins = 30, color="blue",alpha = 0.7, density=True)
        if MV_ou_nonMV == "non-missing values":
            plt.hist(nonSMVList,bins = 30, color="red",alpha = 0.7, density=True)
        if dataSet == "C": 
            plt.title(MV_ou_nonMV+ " ("+str( (indexRatiMV+1)*5) + '% SMV), CityPulse', fontsize = 15 )
        if dataSet == "A": 
            plt.title(MV_ou_nonMV +" ("+str((indexRatiMV+1)*5) + '% SMV), AEP',fontsize = 15)

        plt.yticks([])

        # plt.xlabel(" valeur ")
        plt.xlabel(" value ")

        if MV_ou_nonMV == "imputed values":   
            plt.savefig("figure/" +dataSet+"_InterConfValeur_imputees_"+str(indexRatiMV+1) +"_anglais.png",dpi =500 )
        if MV_ou_nonMV == "non-missing values":
            plt.savefig("figure/" +dataSet+"_InterConfValeur_nonMV_"+str(indexRatiMV+1) +"_anglais.png",dpi =500 )
            print("xxxxxxx")
        plt.show()
