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


def get_filename(path,filetype):  # 输入路径、文件类型例如'.csv'
    name = []
    for root,dirs,files in os.walk(path):
        for i in files:
            if os.path.splitext(i)[1]==filetype:
                name.append(i)    
    return name


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
    # sheet.loc[indexOfResultat,'lock'] = 'locked'    
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


    '''
    获得一个预测误差的分布，按传感器的
    '''
    nomFile_guassiene =   nomFile[indexRatiMV] +"guassiene" +".npy" # 检查文件是否存在，询问是否删除（只是不是“oui”都保留）
    if (os.path.exists(nomFile_guassiene)):
        print('deja existance : ',nomFile_guassiene)
        # if(input(" delete it ?") =="oui" ):
        #     os.remove(nomFile_guassiene)

    if (os.path.exists(nomFile_guassiene)):  # 检查文件是否存在，是的话加载
        err_mean_sensors,err_std_sensors = np.load(nomFile_guassiene, allow_pickle=True)
    else:  # 否则重新计算
        err_mean_sensors = np.zeros(shape=numSensor)
        err_std_sensors = np.zeros(shape=numSensor)
        for i in range(numSensor):
            err_real_Missing = []
            for j in range(indexStar):
                if(E_a_reparer[i][j] != -1 and E_a_reparer[i][j] != -2):
                    err_real_Missing.append(E_prediction[i][j] - E_original[i][j])
            err_mean_sensors[i], err_std_sensors[i] = np.mean(err_real_Missing),np.std(err_real_Missing)
        np.save(nomFile_guassiene, (err_mean_sensors,err_std_sensors))


    '''
    模拟一个信任分数
    '''
    scoreTableau = np.random.randn(numSensor,numIndex)
    scoreCapteurAllHis = np.random.randn( numSensor,numIndex)


    '''
    获取滑动窗口的中的，某个位置的t，某个传感器的过去的值的信任分数的均值
    '''
    def avgScoreWindow(sensorIndex,timeIndex):
        res = scoreTableau[sensorIndex][timeIndex - sizeWin: timeIndex]
        return np.mean(res)

    '''
    计算非缺失值的分数
    '''
    def scoreNonMV(sensorIndex,timeIndex):
        err = E_prediction[sensorIndex][timeIndex] - E_original[sensorIndex][timeIndex]
        err_mean, err_std = err_mean_sensors[sensorIndex], err_std_sensors[sensorIndex]
        score = stats.t.cdf(err, indexStar-1, loc=err_mean, scale=err_std)
        if score > 0.5:
            return (1-score)*2
        else:
            return 2*score


    '''
    获取滑动窗口的中的，某个位置的t，所有定传感器的缺失值比例
    '''
    def ratio_non_MV(sensorIndex,timeIndex):
        ss = E_a_reparer[sensorIndex][timeIndex - sizeWin: timeIndex]
        return 1- (np.sum([ss == -1]) + np.sum([ss == -2]))/sizeWin

    '''
    初始化传感器的信任度均为1
    '''
    scoreCapteur = np.ones(shape=numSensor)


    '''
    获得相关传感器名称，位置，
    获得相关传感器的的信任度的集合
    '''
    def getScoreSensorPertinent(sensorIndex):
        nomsSensorPertinent = VoisinsSensor[sensorIndex] # 获得名字
        indexSensorPertinent =np.reshape( np.array([np.argwhere(indexNomeSensor == x) for x in nomsSensorPertinent]),(1,-1))[0] #获得索引
        scoreSensorPertinent = scoreCapteur[indexSensorPertinent]
        return scoreSensorPertinent

    dddddd = getScoreSensorPertinent(0)


    def G(myArry, m = "avg"):
        if (m == "avg"):
            return np.average(myArry)
        if (m == "min"):
            return np.min(myArry)


    timeStar = time.time()

    scoreEstimed_MV = []
    score_MV = []



    for j in range(indexStar,indexFini):
        timeUsed =round(time.time() - timeStar,0)
        
        progress = round(100*(j-indexStar)/ (indexFini-indexStar),2)
        timeEstimtated = round(100*timeUsed/(progress+0.001),0)
        averageTime = round(timeUsed / (j-indexStar+1 ),6)
        print(progress,"%","timeUsed :",timeUsed , "timeEstimtated",timeEstimtated ,"averageTime ",averageTime,"s  ",j,"form ",indexStar  , "to", indexFini, end="\r")

        for i in range(numSensor):
            scoreCapteur[i] = avgScoreWindow(i,j) * ratio_non_MV(i,j-1)
            scoreCapteurAllHis[i][j] =  avgScoreWindow(i,j) * ratio_non_MV(i,j-1) # 记录所有的传感器信任分数
            if(E_a_reparer[i][j] != -1 and E_a_reparer[i][j] != -2): #非缺失值的处理
                scoreTableau[i][j] = scoreNonMV(i,j)
            else: # 处理缺失值2
                try:
                    test = G(getScoreSensorPertinent(i), m = G_variation)
                    scoreTableau[i][j] = G(getScoreSensorPertinent(i), m = G_variation)
                    if(E_a_reparer[i][j] == -2):       #对于模拟的缺失值 这里记录估计的信任分数和其本来应有的信任分数
                        scoreEstimed_MV.append(scoreTableau[i][j])
                        score_MV.append(scoreNonMV(i,j))
                except:
                    print(getScoreSensorPertinent(i))

    RMSE = mean_squared_error(scoreEstimed_MV,score_MV)

    np.save( "ISTM_resultat/precision/" +dataSet + "_capteurScoreAllhis",scoreCapteurAllHis)

    np.save( "ISTM_resultat/precision/" +dataSet + "_"+  G_variation, (scoreEstimed_MV,score_MV) )


    sheet = pd.read_excel(execel_patch + execel_name, sheet_name= 0,header =0, engine = 'openpyxl')    
    sheet.loc[indexOfResultat,'state'] = "Done"
    sheet.loc[indexOfResultat,'RMSE'] = RMSE
    sheet.loc[indexOfResultat,'lock'] = ''   
    sheet.loc[indexOfResultat,'Time'] = averageTime
    # print("-------averageTime------- ",averageTime)
    sheet.to_excel(execel_patch + execel_name,header =1,index=False)
