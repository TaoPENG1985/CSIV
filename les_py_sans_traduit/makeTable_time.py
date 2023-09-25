from multiprocessing.sharedctypes import Value
import pandas as pd
import numpy as np
import os



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

sheet = pd.read_excel(execel_patch + execel_name, sheet_name= 0,header =0, engine = 'openpyxl')    


def getRMSE_from_sheet(dataSet,indexRatiMV ,minOrMean , winSize):
    for indexOfResultat in range(0,len(sheet)):
        if sheet.iloc[indexOfResultat]['dataSet'] == dataSet and \
            sheet.iloc[indexOfResultat]['indexRatiMV'] == indexRatiMV and \
                sheet.iloc[indexOfResultat]['minOrMean'] == minOrMean and \
                    sheet.iloc[indexOfResultat]['winSize'] == winSize :
            # print(" found")
            return round( sheet.iloc[indexOfResultat]['Time'],4)
    print("non found")


# name_line = ['Proportion MV (%)', 'G', 'w = 5', 'w = 10','w = 15','w = 20', 'w = 25',  'w = 30', ' w optimal', ' RMSE optimal' ]

df = pd.DataFrame()
# print(df.to_latex(index=False))
# winSizeList = [10,30,100,150,200]
winSizeList = [5,10,50,100,150,200]
name_line = [ 'Proportion MV (%)', 'G',]
for  winSize in winSizeList:
    name_line.append("w =" +str(winSize))
name_line.append(' w optimal')
name_line.append(' RMSE optimal')
df[name_line[0]] = name_line[1:]



for minOrMean in ['min', 'avg']:
    # for indexRatiMV in [0,1,2,3,4]:
    for indexRatiMV in [2]:
        colone = []
        colone.append( (indexRatiMV+1)*5)
        colone.append( minOrMean)
        valeurList = []
        for winSize in winSizeList:
            valeurList.append(getRMSE_from_sheet("C",indexRatiMV,minOrMean,winSize))

        minRMSE = np.min(valeurList)
        bestWinSizeIndex =   valeurList.index(minRMSE)
        valeurList.append( winSizeList[bestWinSizeIndex])
        valeurList.append(minRMSE)            


        colone = colone + valeurList
        # print(colone)
        df[str(colone[0]) + colone[1] ] = colone[1:]

print(df.to_latex(index=False))

        





