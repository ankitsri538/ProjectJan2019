import pandas as pa
import numpy as np
import os
import datetime as dt
from dateutil.relativedelta import relativedelta

pathDeliminator = "\\"
folderName = os.getcwd()+pathDeliminator+"InputFiles"
outPutFile = folderName + pathDeliminator + "Result.csv"
masterFileName = "S&P 500 Components.csv"
dateRangeInMonths = [-6,-12]
masterDataFrame = pa.read_csv(folderName+pathDeliminator+masterFileName)
masterDataFrameColumns=['Symbol']
monthList = ['Jan', 'Feb', 'Mar','April','May','Jun','July','Aug','Sept','Oct','Nov','Dec']

def getFileName(postfix = 'Historical Data.csv'):
    uniqueSymbolDataFrame = masterDataFrame[masterDataFrameColumns].stack().unique()
    uniqueNoOfSymbols = len(uniqueSymbolDataFrame)
    print("Processing "+str(uniqueNoOfSymbols)+" files")
    uniqueSymbolDataFrame = [fileName+" "+postfix for fileName in uniqueSymbolDataFrame ]
    return uniqueSymbolDataFrame

def renameColumns(df):
    columnNames = ["Date", "Price","Open","Heigh","Low","Vol","Change Percentage"]
    df.columns = columnNames
    return df

def getPastDate(month = -6,currentDate = dt.date.today()):
    currentDate = getNextWorkingDate(currentDate)
    return currentDate + relativedelta(months=month)

def getNextWorkingDate(toDate = dt.date.today()):
    wd = toDate.weekday() # 0 to 6 .  0 Monday, 6 Sunday

    if wd == 6:
       toDate = dt.datetime(toDate.year,toDate.month,toDate.day+1)
    elif wd == 5:
       toDate = dt.datetime(toDate.year, toDate.month, toDate.day + 2)

    return toDate


def filterRowsBasedOnDate(dataFrame,fromDate,noOfRows = 1,toDate = dt.date.today()):
    fromDate = getPastDate(fromDate,toDate)
    print("date looking from "+str(fromDate))
    print("No of records before filtering "+str(len(dataFrame)))
    dataFrame = dataFrame[dataFrame.Date <= str(fromDate)]
    print("No of records after filtering " + str(len(dataFrame)))
    return  dataFrame[:noOfRows]


#getPastDate()

def getZScore(dataFrame):

       mean = dataFrame.x.mean()
       sd = dataFrame.x.std()
       zScore = dataFrame.x.apply(lambda x: (x-mean)/sd)
       dataFrame['zScore'] = zScore
       print("z score "+str(zScore))
       return dataFrame

def getTickMean(fileName,listOfMissingFiles,priceMeanList,tickNameList,year):

    try:
        dataFrame = pa.read_csv(folderName+pathDeliminator+fileName)
        print("*********************************************************")
        print("processing .... " + fileName)
        columnNames = ["Date","Price"]
        dataFrame = renameColumns(dataFrame)
        filteredDataFrame = dataFrame[columnNames]
        filteredDataFrame.Date = filteredDataFrame.Date.apply(lambda d: dt.datetime.strptime(d, "%b %d, %Y"))
        total =0
        for month in dateRangeInMonths:
            result = filterRowsBasedOnDate(filteredDataFrame, month,1,year)
            total += result.Price
            #print("month "+str(month)+" price " +result.Price)
        meanOfTick = total/len(dateRangeInMonths)
        print("mean "+str(meanOfTick))
        priceMeanList.append(meanOfTick)
        tickNameList.append(fileName.split(" ")[0])
        #print(result)
    except OSError:
        listOfMissingFiles.append(fileName)

def getRankedTick(datafarame,ascending = False, noOfTickes = 50):
    return datafarame.sort_values(by='zScore',ascending=ascending)[:noOfTickes]

def writeIntoFile(fileName,dataFrame):
    dataFrame.to_csv(fileName, sep='\t', encoding='utf-8')

def readFiles(year):
    fileNameList = getFileName()
    listOfMissinfFiles = []
    priceMeanList = []
    tickNameList = []
    for fileName in fileNameList:
         getTickMean(fileName,listOfMissinfFiles,priceMeanList,tickNameList,year)

    if len(listOfMissinfFiles)>0:
        print( str(len(listOfMissinfFiles))+" files missing")
        print("list of files "+str(listOfMissinfFiles))

    xMeanDict = {"tickName":tickNameList,"x":priceMeanList}
    tempDataFrame = pa.DataFrame(data=xMeanDict)
    tempDataFrame = getZScore(tempDataFrame)
    return tempDataFrame

#print(masterDataFrame)

def getDateListForAGivenYear(inputYear):
    monthList = np.arange(12)
    dateList = [dt.datetime(int(inputYear),month+1,1) for month in monthList]
    return dateList

def getYearSpecificResult(dateList):

    for toDate in dateList:
        tempDataFrame = readFiles(toDate)
        monthName = monthList[toDate.month-1]
        outPutFile = folderName + pathDeliminator + "Result_"+monthName+".csv"
        tempDataFrame = getRankedTick(tempDataFrame)
        tempDataFrame = tempDataFrame.tickName
        writeIntoFile(outPutFile,tempDataFrame)


def getResult(isToday = True):
    if not isToday:
        year = input("please enter the year..\n")
        dateList = getDateListForAGivenYear(year)
        getYearSpecificResult(dateList)
    else :
        tempDataFrame = readFiles(dt.date.today());
        writeIntoFile(outPutFile, getRankedTick(tempDataFrame))



#readFiles()

#getResult(False)

getResult(False)
