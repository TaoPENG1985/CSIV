from cmath import nan
from random import random
from tarfile import NUL
from types import resolve_bases
import numpy as np
from pyparsing import alphas
from sklearn import datasets
from sklearn.metrics import mean_squared_error
import math 
from scipy import stats
import os
import time
import pandas as pd
import matplotlib.pyplot as plt

def normfun(x, mu, sigma):
    pdf = np.exp(-((x - mu) ** 2) / (2 * sigma ** 2)) / (sigma * np.sqrt(2 * np.pi))
    return pdf


dataSet = "C"
if dataSet == "C":
    nomFile = ['ISTM_resultat/CityPulse/ISTM_OPM_E_repare_et_E_original_all_BackTime6_modelTestNon5.npy',
                'ISTM_resultat/CityPulse/ISTM_OPM_E_repare_et_E_original_all_BackTime6_modelTestNon10.npy',
                'ISTM_resultat/CityPulse/ISTM_OPM_E_repare_et_E_original_all_BackTime6_modelTestNon15.npy',
                'ISTM_resultat/CityPulse/ISTM_OPM_E_repare_et_E_original_all_BackTime6_modelTestNon20.npy',
                'ISTM_resultat/CityPulse/ISTM_OPM_E_repare_et_E_original_all_BackTime6_modelTestNon25.npy']
if dataSet == "A":
    nomFile = ['ISTM_resultat/AEP/ISTM_OPM_E_repare_et_E_original_all_BackTime4_modelTestNon5.npy',
        'ISTM_resultat/AEP/ISTM_OPM_E_repare_et_E_original_all_BackTime4_modelTestNon10.npy',
        'ISTM_resultat/AEP/ISTM_OPM_E_repare_et_E_original_all_BackTime4_modelTestNon15.npy',
        'ISTM_resultat/AEP/ISTM_OPM_E_repare_et_E_original_all_BackTime4_modelTestNon20.npy',
        'ISTM_resultat/AEP/ISTM_OPM_E_repare_et_E_original_all_BackTime4_modelTestNon25.npy']


# indexRatiMV = 4





for indexRatiMV in [0,1,2,3,4]:
    E_resultat, E_original, E_a_reparer,E_prediction = np.load(nomFile[indexRatiMV], allow_pickle=True)
    numSensor, numIndex = E_resultat.shape
    star = 0.3
    fin  = 0.6
    indexStar = int(numIndex*star)
    indexFini = int(numIndex*fin-1)
    err_real_Missing_all = []
    # for i in range(int(numSensor*0.1)):
    for i in [10]:    
        err_real_Missing = []
        for j in range(indexStar):
            if(E_a_reparer[i][j] != -1 and E_a_reparer[i][j] != -2):
                err_real_Missing.append(E_prediction[i][j] - E_original[i][j])
                err_real_Missing_all.append (E_prediction[i][j] - E_original[i][j])
        # print (np.mean(err_real_Missing),np.std(err_real_Missing)) 

    # print ("all in a set last sensor: ", np.mean(err_real_Missing),np.std(err_real_Missing)) 
    print ("all in a set : " , np.mean(err_real_Missing_all),np.std(err_real_Missing_all)) 

    plt.figure(figsize=(4,6))

    x = np.arange( - np.std(err_real_Missing_all)*2, np.std(err_real_Missing_all)*2, 0.01)
    y = normfun(x, np.mean(err_real_Missing_all), np.std(err_real_Missing_all)*0.79)

    print(y)
    plt.plot(x, y)
    plt.hist(err_real_Missing_all,bins = 100, color="red",alpha = 0.7, density=True)

    plt.xlim(- np.std(err_real_Missing_all)*3, np.std(err_real_Missing_all)*3)



    if dataSet == "C": 
        plt.title(str((indexRatiMV+1)*5) + '% SMV, CityPulse', fontsize = 20 )
    if dataSet == "A": 
        plt.title(str((indexRatiMV+1)*5) + '% SMV, AEP',fontsize = 20)

    plt.yticks([])
    # plt.xlabel('Erreur des valeurs non manquantes',fontsize = 10)
    plt.xlabel('Error of non-missing values',fontsize = 20)

    # plt.ylabel('Probabilité',fontsize = 10)


    plt.savefig("figure/" +dataSet+"_"+str(indexRatiMV+1) +"_anglais.png",dpi =500 )
    plt.show()

    # print ('stats.kstest ',stats.kstest(err_real_Missing_all, 'norm'))


# x = np.arange( - np.std(err_real_Missing)*5, np.std(err_real_Missing)*5,0.01)
# y = normfun(x, np.mean(err_real_Missing), np.std(err_real_Missing)*0.4)

# plt.plot(x, y)

# plt.hist(err_real_Missing,bins = 100, color="red",alpha = 0.7,density=True)

# plt.xlim(- np.std(err_real_Missing)*5, np.std(err_real_Missing)*5)

# plt.title('Length distribution')
# plt.xlabel('Length')
# plt.ylabel('Probability')

# plt.show()
