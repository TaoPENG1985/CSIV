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



nomFileC = ['ISTM_resultat/CityPulse/ISTM_OPM_E_repare_et_E_original_all_BackTime6_modelTestNon5.npy',
            'ISTM_resultat/CityPulse/ISTM_OPM_E_repare_et_E_original_all_BackTime6_modelTestNon10.npy',
            'ISTM_resultat/CityPulse/ISTM_OPM_E_repare_et_E_original_all_BackTime6_modelTestNon15.npy',
            'ISTM_resultat/CityPulse/ISTM_OPM_E_repare_et_E_original_all_BackTime6_modelTestNon20.npy',
            'ISTM_resultat/CityPulse/ISTM_OPM_E_repare_et_E_original_all_BackTime6_modelTestNon25.npy']

nomFileA = ['ISTM_resultat/AEP/ISTM_OPM_E_repare_et_E_original_all_BackTime4_modelTestNon5.npy',
'ISTM_resultat/AEP/ISTM_OPM_E_repare_et_E_original_all_BackTime4_modelTestNon10.npy',
'ISTM_resultat/AEP/ISTM_OPM_E_repare_et_E_original_all_BackTime4_modelTestNon15.npy',
'ISTM_resultat/AEP/ISTM_OPM_E_repare_et_E_original_all_BackTime4_modelTestNon20.npy',
'ISTM_resultat/AEP/ISTM_OPM_E_repare_et_E_original_all_BackTime4_modelTestNon25.npy']

nomFile = [nomFileC,nomFileA]

df = pd.DataFrame()


df["  "] = ['Proportion MV (%)', 'espérance','écart-type']

for i in [0,1]:
    for indexRatiMV in [0,1,2,3,4]:
        nomFile_guassiene =   nomFile[i][indexRatiMV] +"guassiene" +".npy"
        err_mean_sensors,err_std_sensors = np.load(nomFile_guassiene, allow_pickle=True)
        err_mean_sensors = np.average(err_mean_sensors)
        err_std_sensors = np.average(err_std_sensors)
        df[str(i) + "" + str(indexRatiMV)] = [ int(indexRatiMV+1)*5, round (err_mean_sensors,2),round( err_std_sensors,2)]

print(df.to_latex(index=False))
