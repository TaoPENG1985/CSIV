from tarfile import NUL
from types import resolve_bases
import numpy as np
# from sklearn.metrics import mean_squared_error
import math 
from scipy import stats
import os
import time
import pandas as pd
from A001_fonctions import * 

'''
Note : Vous devez télécharger <ISTM_result> dans ce projet (voir email). 
<ISTM_result> est un dossier contenant les résultats MIST qui constituent les données d'entrée du projet.

Le programme extrait les paramètres du fichier Excel et calcule les résultats, qui sont stockés dans le fichier Excel.
'''

# ===================================================================
# Nous stockons les paramètres et les résultats dans un fichier Excel.
# Nous dressons la liste de tous les fichiers Excel et laissons l'utilisateur en choisir un.
# 
# Le schema des Excel sont comme suivant:
#(1) Stat = <Done, norDone> :  indique si le jeu de paramètres a déjà été calculé ou non.
#(2) lock = <locked> ou vide: si la ligne actuelle (un ensemble de paramètres) est en cours de calcul, 
#   si c'est "locked", elle doit être ignorée pour éviter de répéter le calcul et de gaspiller des ressources informatiques.
#(3) star: Point de départ de l'ensemble de données
#(4) fin : Endroit où l'ensemble de données se termine
#(5) dataSet = <A,C>. A est l'ensemble de données AEP et C est l'ensemble de données cityPulse.
#(6) indexRatiMV : est le numéro de séquence de l'ensemble de données ,
#    par exemple 0 pour un ratio de valeurs manquantes simulé de 5 %, 4 pour un 25 %.
#(7) minOrMean : 
#(8) winSize : la taile de fenetre
#(9) RMSE : la Performance  de CSIV
# ===================================================================
execel_patch = "excel_para_resultat/"
file_Nmae = get_filename(execel_patch, '.xlsx')
for i in range(len(file_Nmae)):
    print(i, '   ', file_Nmae[i])
execel_name = file_Nmae[int(input('Sélectionnez un fichier EXCEL, entrez le numéro de série et appuyez sur la touche Entrée pour confirmer.'))]
print('vous avez sélectionné :', execel_name)

# ===================================================================
# Extraire les paramètres d'un fichier Excel et calculer les résultats, qui sont stockés dans le fichier excel.
# ===================================================================
while(True):
    # Si toutes les combinaisons de paramètres dans ce fichier ont déjà un résultat (marqué comme Done),
    #  la boucle se termine, c'est-à-dire que la tâche s'achève. 
    sheet = pd.read_excel(execel_patch + execel_name, sheet_name= 0,header =0, engine = 'openpyxl')    
    if 'notDone' not in sheet.values:
        break
    
    # Si recuperer les papramètre des 1er linge qui est <notDone>
    # puis recuperer les le fich de npy selons les papramètres
    for indexOfResultat in range(0,len(sheet)):
        if sheet.iloc[indexOfResultat]['state'] == 'notDone':
            print('indexOfResultat ',indexOfResultat)
            sizeWin  = sheet.iloc[indexOfResultat]['winSize']
            indexRatiMV  = sheet.iloc[indexOfResultat]['indexRatiMV']
            minOrMean = sheet.iloc[indexOfResultat]['minOrMean']
            star = sheet.iloc[indexOfResultat]['star']
            fin = sheet.iloc[indexOfResultat]['fin']
            dataSet = sheet.iloc[indexOfResultat]['dataSet']
            break

    # (1)nomFile : recuperer le fich de npy selons les papramètres
    # (2)VoisinsSensor : Obtenir le numéro du capteur et de ses voisins.
    # (3) indexNomeSensor :  Obtenir le numéro du capteur.
    # (4)decomposer le fich de npy en 4:
    # E_resultat : Contient un ensemble de données sur les résultats prédits avec toutes les valeurs manquantes fixées.) 
    # E_original :est la donnée originale contenant les valeurs manquantes originales (dénotées par -1) 
    # E_a_reparer : Contient des valeurs non manquantes, Contient des valeurs manquantes brutes (dénotées par -1), Contient des valeurs manquantes simulées (dénotées par -2) ) 
    # E_prediction : Contient toutes les valeurs prédites
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

    VoisinsSensor = np.load(tousLesVoisinsDeTouslesPionts, allow_pickle=True)
    indexNomeSensor = np.array ([x[0] for x in VoisinsSensor])
    E_resultat, E_original, E_a_reparer,E_prediction = np.load(nomFile[indexRatiMV], allow_pickle=True)



    #Les données précédant l'indexStar sont utilisées pour initialiser le
    #Les données entre indexStar et indexFini sont utilisées pour calculer le résultat final. 
    numSensor, numIndex = E_resultat.shape
    indexStar = int(numIndex*star)
    indexFini = int(numIndex*fin-1)


    # En utilisant les données avant l'indexStar, 
    # nous calculons la distribution de l'erreur de prédiction pour chaque capteur et la stockons.    
    nomFile_guassiene =   nomFile[indexRatiMV] +"guassiene" +".npy" 
    if (os.path.exists(nomFile_guassiene)):  # Vérifier si le fichier existe, et le charger si c'est le cas
        print('deja existance : ',nomFile_guassiene)
        err_mean_sensors,err_std_sensors = np.load(nomFile_guassiene, allow_pickle=True)
    else:  # Sinon, recalculer
        err_mean_sensors = np.zeros(shape=numSensor)
        err_std_sensors = np.zeros(shape=numSensor)
        for i in range(numSensor):
            err_real_Missing = []
            for index_time in range(indexStar):
                if(E_a_reparer[i][index_time] != -1 and E_a_reparer[i][index_time] != -2):
                    err_real_Missing.append(E_prediction[i][index_time] - E_original[i][index_time])
            err_mean_sensors[i], err_std_sensors[i] = np.mean(err_real_Missing),np.std(err_real_Missing)
        np.save(nomFile_guassiene, (err_mean_sensors,err_std_sensors))

    # 建立一个接受最终结果举证，其填满了随机数字。这些随机数字将会被计算结果取代
    scoreTableau = np.random.randn(numSensor,numIndex)

    # Le niveau de confiance du capteur est initialement de 1
    scoreCapteur = np.ones(shape=numSensor)


    # 1 avgScoreWindow :Calculer la moyenne des scores dans la fenêtre pour un capteur cilbé 
    def avgScoreWindow(sensorIndex,timeIndex):
        res = scoreTableau[sensorIndex][timeIndex - sizeWin: timeIndex]
        return np.mean(res)
    # 2 scoreNonMV :  Pour une valeur non manquante, calculer le score de confiance pour sa valeur prédite 
    def scoreNonMV(sensorIndex,timeIndex):
        err = E_prediction[sensorIndex][timeIndex] - E_original[sensorIndex][timeIndex]
        err_mean, err_std = err_mean_sensors[sensorIndex], err_std_sensors[sensorIndex]
        score = stats.t.cdf(err, indexStar-1, loc=err_mean, scale=err_std)
        if score > 0.5:
            return (1-score)*2
        else:
            return 2*score
    # 3 ratio_non_MV :Calculer la proportion de valeurs non manquantes dans la fenêtre, pour un capteur cilbé 
    def ratio_non_MV(sensorIndex,timeIndex):
        ss = E_a_reparer[sensorIndex][timeIndex - sizeWin: timeIndex]
        return 1- (np.sum([ss == -1]) + np.sum([ss == -2]))/sizeWin

    # 4 getScoreSensorPertinent: Obtenir le nom et l'emplacement des capteurs concernés, et 
    # renvoyer l'ensemble des niveaux de confiance des capteurs concernés.
    def getScoreSensorPertinent(sensorIndex):
        nomsSensorPertinent = VoisinsSensor[sensorIndex] # 获得名字
        indexSensorPertinent =np.reshape( np.array([np.argwhere(indexNomeSensor == x) for x in nomsSensorPertinent]),(1,-1))[0] #获得索引
        scoreSensorPertinent = scoreCapteur[indexSensorPertinent]
        return scoreSensorPertinent

    # 5 getScoreSensor: Renvoie la moyenne ou le minimum de l'ensemble des niveaux de confiance des capteurs concernés.
    def getScoreSensor(myArry, m = "avg"):
        if (m == "avg"):
            return np.average(myArry)
        if (m == "min"):
            return np.min(myArry)


    timeStar = time.time()

    score_CSIV = [] # les socre de confiance selons CSIV 
    score_souhaite = [] # les socre de confiance si on sais le valeur des donnes manquantes

    # Commencer à parcourir chronologiquement
    for index_time in range(indexStar,indexFini):
        # Afficher l'état d'avancement
        timeUsed =round(time.time() - timeStar,0)
        progress = round(100*(index_time-indexStar)/ (indexFini-indexStar),2)
        timeEstimtated = round(100*timeUsed/(progress+0.001),0)
        print(progress,"%","timeUsed :",timeUsed , "timeEstimtated",timeEstimtated ,index_time,"form ",indexStar  , "to", indexFini, end="\r")

        # Commencer à parcourir les capteurs
        for i in range(numSensor):
            # caculer  / mettre a jour le score de confiance d'un capteur 
            scoreCapteur[i] = avgScoreWindow(i,index_time) * ratio_non_MV(i,index_time-1)
            # pour les valeurs bien recues (non manquante)
            if(E_a_reparer[i][index_time] != -1 and E_a_reparer[i][index_time] != -2): 
                scoreTableau[i][index_time] = scoreNonMV(i,index_time)
            # Valeurs manquantes réelles et valeurs manquantes simulées
            else: 
                try:
                    scoreTableau[i][index_time] = getScoreSensor(getScoreSensorPertinent(i), m = minOrMean)
                    if(E_a_reparer[i][index_time] == -2):      
                        score_CSIV.append(scoreTableau[i][index_time])
                        score_souhaite.append(scoreNonMV(i,index_time))
                except:
                    print(getScoreSensorPertinent(i))

    MSE_CSIV_shouaite = np.square(np.subtract(score_CSIV,score_souhaite)).mean() 
    RMSE_CSIV_shouaite = math.sqrt(MSE_CSIV_shouaite)

    # Enregistrer les résultats dans Excel
    sheet.loc[indexOfResultat,'state'] = "Done"
    sheet.loc[indexOfResultat,'RMSE'] = RMSE_CSIV_shouaite
    sheet.to_excel(execel_patch + execel_name,header =1,index=False)
