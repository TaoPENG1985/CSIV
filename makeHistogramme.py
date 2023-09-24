min_AEP = [0.13, 0.15, 0.16, 0.18 , 0.21]
avg_AEP = [0.08,0.09,0.09,0.11,0.12]

min_City =[0.17,0.19,0.20,0.23,0.26]
avg_City =[0.09,0.1,0.11,0.12,0.14]

import matplotlib.pyplot as plt
import numpy as np 


plt.figure(figsize=(6,5.5))
x = [1,2,3,4,5]

rects1 = plt.bar([i - 0.1 for i in x], height=min_AEP, width=0.5, alpha=0.8, color='red', label="SCIV_min")
rects2 = plt.bar([i + 0.1 for i in x], height=avg_AEP, width=0.4, color='green', label="SCIV_average")
plt.xlabel("(a) Proportion de valeurs manquantes dans le jeu des données AEP")
plt.xlabel("(a)Proportion of missing values, AEP", size = 15)

# rects3 = plt.bar([i - 0.1 for i in x], height=min_City, width=0.5, alpha=0.8, color='red', label="SCIV_min")
# rects4 = plt.bar([i + 0.1 for i in x], height=avg_City, width=0.4, color='green', label="SCIV_average")
# plt.xlabel("(b) Proportion de valeurs manquantes dans le jeu des données CityPulse")
# plt.xlabel("(b)Proportion of missing values, CityPulse", size = 15)

plt.ylim(0, 0.3)     # y轴取值范围
plt.ylabel("RMSE")

label_list = [ "5%" ,"10 %" ,"15%" ,"20 %" ,"25 %" ]
plt.xticks(x, label_list, rotation=0)
plt.legend() 

plt.show()