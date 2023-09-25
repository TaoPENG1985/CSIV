from cmath import nan
from random import random
from tarfile import NUL
from types import resolve_bases
import numpy as np
import math 
from scipy import stats
import os
import time
import pandas as pd
from A001_fonctions import *
'''



'''

# ===================================================================
#  
# 
# ===================================================================
execel_patch = "ISTM_resultat/CityPulse/"
file_Nmae = get_filename(execel_patch, '.xlsx')
for i in range(len(file_Nmae)):
    print(i, '   ', file_Nmae[i])
execel_name = file_Nmae[int(input(' give index of file'))]
print('execel_name :', execel_name)

while(True):
    sheet = pd.read_excel(execel_patch + execel_name, sheet_name= 0,header =0, engine = 'openpyxl')    
    if 'notDone' not in sheet.values:
        break

    # 获得未处理且未锁定的项目
    list_unLock = []
    for indexOfResultat in range(0,len(sheet)):
        if sheet.iloc[indexOfResultat]['state'] == 'notDone' and sheet.iloc[indexOfResultat]['lock'] != "locked":
            list_unLock.append(indexOfResultat)
        # if len(list_unLock) > 20 :
            # list_unLock = list_unLock[:20]

    
    indexOfResultat =np.random.choice(list_unLock) 
    sheet.loc[indexOfResultat,'lock'] = 'locked'    
    print('         indexOfResultat '  ,indexOfResultat+2, ".........................")
    sizeWin  = sheet.iloc[indexOfResultat]['winSize']
    indexRatiMV  = sheet.iloc[indexOfResultat]['indexRatiMV']
    G_variation = sheet.iloc[indexOfResultat]['minOrMean']
    star = sheet.iloc[indexOfResultat]['star']
    fin = sheet.iloc[indexOfResultat]['fin']
    dataSet = sheet.iloc[indexOfResultat]['dataSet']
    # 完成锁定
    sheet.to_excel(execel_patch + execel_name,header =1,index=False)



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

    '''
    确认窗口大小，开始位置（30%，之前的确认分布参数），结束位置就是最后一个
    '''
    numSensor, numIndex = E_resultat.shape
    indexStar = int(numIndex*star)
    indexFini = int(numIndex*fin-1)



    timeStar = time.time()

    errNonMVList = []
    errSMVLsit =  []
    SMVLsit = []

    for  j in range(indexStar-sizeWin,indexStar):
        for i in range(numSensor):
            if (E_a_reparer[i][j]  == -2): #模拟缺失值
                errSMVLsit.append(E_prediction[i][j] - E_original[i][j])
                SMVLsit.append(E_prediction[i][j])
            if(E_a_reparer[i][j] != -1 and E_a_reparer[i][j] != -2):
                errNonMVList.append(E_prediction[i][j] - E_original[i][j])
            

    for j in range(indexStar,indexFini):
        timeUsed =round(time.time() - timeStar,0)

        progress = round(100*(j-indexStar)/ (indexFini-indexStar),2)
        timeEstimtated = round(100*timeUsed/(progress+0.001),0)
        averageTime = round(timeUsed / (j-indexStar+1 ),6)
        print(progress,"%","timeUsed :",timeUsed , "timeEstimtated",timeEstimtated ,"averageTime ",averageTime,"s  ",j,"form ",indexStar  , "to", indexFini, end="\r")

        

        for i in range(numSensor):
            if(E_a_reparer[i][j]  == -2): #模拟缺失值的处理 
                errSMVLsit.pop(0)
                errSMVLsit.append(E_prediction[i][j] - E_original[i][j])
                SMVLsit.pop(0)
                SMVLsit.append(E_prediction[i][j])
                E_prediction[i][j]
            if(E_a_reparer[i][j] != -1 and E_a_reparer[i][j] != -2):
                errNonMVList.pop(0)
                errNonMVList.append(E_prediction[i][j] - E_original[i][j])
        
        err_mean_SMV , std_mean_SMV = np.mean(errSMVLsit) , np.std(errSMVLsit)
        err_mean_nonMV , std_mean_nonMV = np.mean(errNonMVList) , np.std(errNonMVList)

        conf_interal_nonMV = stats.norm.interval(0.95, loc= err_mean_nonMV, scale = std_mean_nonMV)
        conf_interal_SMV = stats.norm.interval(0.95, loc= err_mean_SMV, scale = std_mean_SMV)
        

        # print( "conf_interal_nonMV ",conf_interal_nonMV )
        # print ("conf_interal_nonMV ",stats.kstest(conf_interal_SMV, 'norm'))

        # print( "conf_interal_SMV ",conf_interal_SMV )
        # print ("conf_interal_SMV ",stats.kstest(conf_interal_SMV, 'norm'))

        # print( "SMVLsit ",SMVLsit )
        print ("SMVLsit ",stats.kstest(SMVLsit, 'norm'))  




    # np.save( "ISTM_resultat/precision/" +dataSet + "_"+  G_variation, (scoreEstimed_MV,score_MV) )


    sheet = pd.read_excel(execel_patch + execel_name, sheet_name= 0,header =0, engine = 'openpyxl')    
    sheet.loc[indexOfResultat,'state'] = "Done"
    # sheet.loc[indexOfResultat,'RMSE'] = RMSE
    sheet.loc[indexOfResultat,'lock'] = ''   
    sheet.loc[indexOfResultat,'Time'] = averageTime
    # print("-------averageTime------- ",averageTime)
    sheet.to_excel(execel_patch + execel_name,header =1,index=False)
