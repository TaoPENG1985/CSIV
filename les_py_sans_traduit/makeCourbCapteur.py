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


dataSet = "C" 
if(dataSet == "C"):
    nomFile = "ISTM_resultat/precision/C_capteurScoreAllhis.npy"
    tousLesVoisinsDeTouslesPionts = 'ISTM_resultat/CityPulse/tousLesVoisinsDeTouslesPionts.npy'
elif(dataSet == "A"): 
    nomFile = "ISTM_resultat/precision/A_capteurScoreAllhis.npy"
    tousLesVoisinsDeTouslesPionts = 'ISTM_resultat/AEP/tousLesVoisinsDeTouslesPionts_RH_TH.npy'


scoreCapteurAllHis = np.load(nomFile, allow_pickle=True)

winSzie = 1000
numSensor, numIndex = scoreCapteurAllHis.shape
star = 0.4 
fin = 0.6
indexStar = int(numIndex*star) 
indexFini = int(numIndex*fin-1)
scoreCapteurAllHis = scoreCapteurAllHis[:,indexStar + 2000 : indexStar +  2000 +winSzie]

VoisinsSensor = np.load(tousLesVoisinsDeTouslesPionts, allow_pickle=True)
indexNomeSensor = np.array ([x[0] for x in VoisinsSensor])

indexSensor = 0
nomsSensorPertinent = np.array( VoisinsSensor[indexSensor])
indexSensorPertinent = np.reshape([np.argwhere(indexNomeSensor == x) for x in nomsSensorPertinent],(1,-1))[0]

# 

# scoreCapteurAllHis = np.random.randn( numSensor,500)

plt.figure(figsize=(10,4))
for i in range(len(nomsSensorPertinent)):
    plt.subplot(len(nomsSensorPertinent),1,i+1)
    plt.plot(range(len(scoreCapteurAllHis[i])), scoreCapteurAllHis[i], color = 'red', label = "# " + str(nomsSensorPertinent[i]),linewidth=1)
    plt.legend(loc='center right')
    plt.ylim(0, 1) 
    if i == len(nomsSensorPertinent)-1:
        plt.xticks(range(0,winSzie , winSzie //2 ), ["02-05-2014","03-05-2014"] )
    else:
        plt.xticks([])
    
    plt.yticks([0, 0.5, 1], [" ","0.5",'1'] )




plt.show()
