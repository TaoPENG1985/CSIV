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
import matplotlib.pyplot as plt

A_avg= "ISTM_resultat/precision/A_avg.npy"
A_min= "ISTM_resultat/precision/A_min.npy"
C_avg= "ISTM_resultat/precision/C_avg.npy"
C_min= "ISTM_resultat/precision/C_min.npy"

A_avg,A_avg_orginal  = np.load(A_avg, allow_pickle=True)
A_min,A_min_orginal  = np.load(A_min, allow_pickle=True)
C_avg,C_avg_orginal  = np.load(C_avg, allow_pickle=True)
C_min,C_min_orginal  = np.load(C_min, allow_pickle=True)

def traite (L,L_org, star, num):
    res = []
    res_org = []
    count = 0
    for i in range(star,len(L_org)):
        if L_org[i] > 0.1 and L_org[i]< 0.9:
            res.append(L[i])
            res_org.append(L_org[i])
            count +=1
        if count >= num:
            break

    return np.array(res),np.array(res_org)

star = 8000
num = 1000


A_avg,A_avg_orginal = traite (A_avg,A_avg_orginal, star, num)
A_min,A_min_orginal = traite (A_min,A_min_orginal, star, num)
C_avg,C_avg_orginal = traite (C_avg,C_avg_orginal, star, num)
C_min,C_min_orginal = traite (C_min,C_min_orginal, star, num)


plt.figure(figsize=(10,3))
plt.ylim(-0.1, 1) 

# # plt.plot(range(0,num),A_min_orginal,  label = 'attendu',color='black')
# plt.plot(range(0,num),A_min_orginal,  label = 'expected values',color='black')
# plt.plot(range(0,num),A_avg,  label = 'SCIV_average',color='green')
# plt.plot(range(0,num),A_min,  label = 'SCIV_min',color='red')
# plt.xticks(range(0,num,500), ["01-04-2016","02-04-2016"]  )
# # plt.xlabel('(a) le jeu des données AEP ')
# plt.xlabel('(a)  AEP ')

# plt.plot(range(0,num),C_min_orginal,  label = 'attendu',color='black')
plt.plot(range(0,num),C_min_orginal,  label = 'expected values',color='black')
plt.plot(range(0,num),C_avg,  label = 'SCIV_average',color='green')
plt.plot(range(0,num),C_min,  label = 'SCIV_min',color='red')
plt.xticks(range(0,num,500), ["02-05-2014","03-05-2014"]  )
# plt.xlabel('(b) dans le jeu des données CityPulse ')
plt.xlabel('(b) CityPulse ')


# plt.plot(range(star,end),C_min_orginal[star:end],  label = 'socre de confiance',color='black')

# plt.xticks(xx, range(1,len(xx)+1))
# plt.ylabel('socre de confiance')
plt.ylabel('confidence score')

# plt.xlabel('Temps ')

plt.legend()
plt.tight_layout()

# plt.savefig('/Users/taopeng/Dropbox/应用/Overleaf/These de Tao/fig/chapitre_4_figure/figure_avec_Time_6.png', 
#             dpi=600,
#            )
plt.show()

