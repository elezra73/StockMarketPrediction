import pandas as pd
import statistics
# from pandas import Series
import os
from matplotlib import pyplot as plt

import pyEX as p


# series = Series.from_csv('Apple Stock Daily - 1.1.2012 ~ 2.4.2019.csv', header=0, index_col=5, parse_dates=True)

# ***** This function get fileName as input, create folder and return the path *****#
def Create_Deployment(FolderName):
    try:
        print(FolderName)
        os.mkdir(FolderName)
    except OSError:
        print("Creation Error, Directory already exist")
        # exit()
    else:
        print("Successfully created the directory")

    full_path = os.path.realpath(__file__)
    path, filename = os.path.split(full_path)
    path = os.path.join(path, FolderName)
    return path


# **** Linear Interpolation Algorithm ****#
def CreateDataWithLinearInterpolation(CsvFilePath, PeriodOfTime, Deployment_Path):
    Close = pd.read_csv(CsvFilePath, usecols=["Close"])
    Date = pd.read_csv(CsvFilePath, usecols=["Date"])

    Close_List = []
    Data_List = []
    for row in Close.itertuples(index=True, name='Close'):
        Close_List.append(getattr(row, "Close"))  # Create List of 'close' data

    for row in Date.itertuples(index=True, name='Date'):
        Data_List.append(getattr(row, "Date"))  # Create List of 'close' data

    Close_Tuples = tuple(Close_List[i: i + PeriodOfTime] for i in range(0, len(Close), PeriodOfTime - 1))
    Date_Tuples = tuple(Data_List[i: i + PeriodOfTime] for i in range(0, len(Date), PeriodOfTime - 1))

    for i, j in zip(Close_Tuples, Date_Tuples):
        try:
            plt.figure(j[0] + ' ~ ' + j[PeriodOfTime - 1])
        except IndexError:
            break
        plt.plot(legend=None)
        # plt.axis('off')
        plt.plot(j, i)
        plt.axis('off')
        plt.savefig(os.path.join(Deployment_Path, j[0] + ' ~ ' + j[PeriodOfTime - 1]))
        plt.close()

    # Close.plot(legend=None)
    # plt.axis('off')
    # plt.show()


# ***** MAM Algorithm *****#
def CreateDataWithMovingAverageMapping(CsvFilePath, PeriodOfTime, Deployment_Path):
    Close = pd.read_csv(CsvFilePath, usecols=["Close"])
    Date = pd.read_csv(CsvFilePath, usecols=["Date"])

    Close_List = []
    Data_List = []
    for row in Close.itertuples(index=True, name='Close'):
        Close_List.append(getattr(row, "Close"))  # Create List of 'close' data

    for row in Date.itertuples(index=True, name='Date'):
        Data_List.append(getattr(row, "Date"))  # Create List of 'close' data

    Close_Tuples = tuple(Close_List[i: i + PeriodOfTime] for i in range(0, len(Close), PeriodOfTime - 1))
    Date_Tuples = tuple(Data_List[i: i + PeriodOfTime] for i in range(0, len(Date), PeriodOfTime - 1))

    for i, j in zip(Close_Tuples, Date_Tuples):
        try:
            plt.figure(j[0] + ' ~ ' + j[PeriodOfTime - 1])
        except IndexError:
            break
        plt.plot(legend=None)
        # print(pd.DataFrame(i))
        plt.plot(j, i)
        rolling_mean = pd.DataFrame(i).rolling(window=5).mean()  # TODO min_periods=1
        # print(rolling_mean)
        plt.axis('off')
        plt.plot(j, rolling_mean)
        Moves = 0
        for x in range(PeriodOfTime):
            try:
                Moves = Moves + i[x + 1] - i[x]
            except IndexError:
                continue

        # if statistics.mean(Close_Tuples[cnt+1]) > statistics.mean(Close_Tuples[cnt]):  #TODO Another way for decide Up/Down
        if Moves > 0:
            print('Up')
            plt.savefig(os.path.join(Deployment_Path, 'Up', j[0] + ' ~ ' + j[PeriodOfTime - 1] + '.jpg'))  # Up
        else:
            print('Down')
            plt.savefig(os.path.join(Deployment_Path, 'Down', j[0] + ' ~ ' + j[PeriodOfTime - 1] + '.jpg'))  # Down

        plt.close()


# **** DMAM Algorithm *****#
def CreateDataWithDoubleMovingAverageMapping(CsvFilePath, PeriodOfTime, Deployment_Path):
    Close = pd.read_csv(CsvFilePath, usecols=["Close"])
    Date = pd.read_csv(CsvFilePath, usecols=["Date"])

    Close_List = []
    Data_List = []
    for row in Close.itertuples(index=True, name='Close'):
        Close_List.append(getattr(row, "Close"))  # Create List of 'close' data

    for row in Date.itertuples(index=True, name='Date'):
        Data_List.append(getattr(row, "Date"))  # Create List of 'close' data

    Close_Tuples = tuple(Close_List[i: i + PeriodOfTime] for i in range(0, len(Close), PeriodOfTime - 1))
    Date_Tuples = tuple(Data_List[i: i + PeriodOfTime] for i in range(0, len(Date), PeriodOfTime - 1))

    for i, j in zip(Close_Tuples, Date_Tuples):
        try:
            plt.figure(j[0] + ' ~ ' + j[PeriodOfTime - 1])
        except IndexError:
            break
        plt.plot(legend=None)
        print(pd.DataFrame(i))
        rolling_mean = pd.DataFrame(i).rolling(window=5).mean()  # TODO fix chunk of mean calculation every 5 pices
        print(rolling_mean)
        plt.plot(j, rolling_mean)
        plt.savefig(os.path.join(Deployment_Path, j[0], ' ~ ' + j[PeriodOfTime - 1]))
        plt.close()


# *****Main Function: this function get full path of .csv file, Method transformation and Period of time for the pictures range*****#
def Main(CsvFileName, Method, PeriodOfTime):
    CsvFilePath = CsvFileName[: len(CsvFileName) - 4:]
    Deployment_Path = Create_Deployment(CsvFilePath)
    print(Deployment_Path)

    if Method == 'Linear Interpolation':
        Linear_Path = os.path.join(Deployment_Path, 'Linear Interpolation')
        Create_Deployment(Linear_Path)
        CreateDataWithLinearInterpolation(CsvFileName, PeriodOfTime, Linear_Path)

    if Method == 'Moving Average Mapping' or Method == 'MAM':
        MAM_Path = os.path.join(Deployment_Path, 'Moving Average Mapping')
        print(MAM_Path)
        Create_Deployment(MAM_Path)
        Create_Deployment(os.path.join(MAM_Path, 'Up'))
        Create_Deployment(os.path.join(MAM_Path, 'Down'))
        CreateDataWithMovingAverageMapping(CsvFileName, PeriodOfTime, MAM_Path)

    if Method == 'Double Moving Average Mapping' or Method == 'DMAM':
        DMAM_Path = os.path.join(Deployment_Path, 'Double Moving Average Mapping')
        Create_Deployment(DMAM_Path)
        CreateDataWithDoubleMovingAverageMapping(CsvFileName, PeriodOfTime, DMAM_Path)

    if Method == 'Gramian Angular Field' or 'GAF':
        print('TODO')
        # CreateDataWithMovingAverageMapping(CsvFileName, PeriodOfTime)


Main("Apple Stock Daily - 1.1.2012 ~ 2.4.2019.csv", 'MAM', 10)
Main("Elbit Stock Daily - 1.1.2012 _ 2.4.2019.csv", 'MAM',10)
Main("Intel Stock Daily - 1.1.2012 _ 2.4.2019.csv", 'MAM',10)
# Main("Apple Stock Daily - 1.1.2012 ~ 2.4.2019.csv", 'Linear Interpolation',10)      #TODO get this value as input from user
