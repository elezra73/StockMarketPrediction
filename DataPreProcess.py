import numpy as np
from mpl_toolkits.axes_grid1 import ImageGrid
from pyts.image import GramianAngularField
import math
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
        Moves = 0
        for x in range(PeriodOfTime):
            try:
                Moves = Moves + i[x + 1] - i[x]
            except IndexError:
                continue
        try:
            if Moves > 0:
                plt.savefig(os.path.join(Deployment_Path, 'Up', j[0] + ' ~ ' + j[PeriodOfTime - 1] + '.jpg'))  # Up
            else:
                plt.savefig(os.path.join(Deployment_Path, 'Down', j[0] + ' ~ ' + j[PeriodOfTime - 1] + '.jpg'))  # Down
        except IndexError:
            break

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
        plt.plot(j, i)                          #plot linear interpolation
        rolling_mean = pd.DataFrame(i).rolling(window=5,min_periods=1).mean()  # TODO min_periods=1
        # print(rolling_mean)
        plt.axis('off')
        plt.plot(j, rolling_mean)               #plot MAM
        Moves = 0
        for x in range(PeriodOfTime):
            try:
                Moves = Moves + i[x + 1] - i[x]
            except IndexError:
                continue

        # if statistics.mean(Close_Tuples[cnt+1]) > statistics.mean(Close_Tuples[cnt]):  #TODO Another way for decide Up/Down
        if Moves > 0:
            plt.savefig(os.path.join(Deployment_Path, 'Up', j[0] + ' ~ ' + j[PeriodOfTime - 1] + '.jpg'))  # Up
        else:
            plt.savefig(os.path.join(Deployment_Path, 'Down', j[0] + ' ~ ' + j[PeriodOfTime - 1] + '.jpg'))  # Down

        plt.close()


# **** DMAM Algorithm *****#
def CreateDataWithDoubleMovingAverageMapping(CsvFilePath, PeriodOfTime, Deployment_Path):
    Close = pd.read_csv(CsvFilePath, usecols=["Close"])
    Open = pd.read_csv(CsvFilePath, usecols=["Open"])
    Date = pd.read_csv(CsvFilePath, usecols=["Date"])

    Open_List = []
    Close_List = []
    Data_List = []

    for row in Open.itertuples(index=True, name='Open'):
        Open_List.append(getattr(row, "Open"))  # Create List of 'Open' data

    for row in Close.itertuples(index=True, name='Close'):
        Close_List.append(getattr(row, "Close"))  # Create List of 'close' data

    for row in Date.itertuples(index=True, name='Date'):
        Data_List.append(getattr(row, "Date"))  # Create List of 'Date' data

    Open_Tuples = tuple(Open_List[i: i + PeriodOfTime] for i in range(0, len(Open), PeriodOfTime - 1))
    Close_Tuples = tuple(Close_List[i: i + PeriodOfTime] for i in range(0, len(Close), PeriodOfTime - 1))
    Date_Tuples = tuple(Data_List[i: i + PeriodOfTime] for i in range(0, len(Date), PeriodOfTime - 1))
    for i, j, k in zip(Close_Tuples, Date_Tuples, Open_Tuples):
        try:
            plt.figure(j[0] + ' ~ ' + j[PeriodOfTime - 1])          #Naming the deployment picture
        except IndexError:
            break

        mean_list = []
        for size in range(PeriodOfTime):
            mean_list.append((i[size] + k[size]) / 2)                                  #Calculate mean between Open & Close
        plt.axis('off')
        plt.plot(j,i,color='green')                      #TODO , add Linear interpolation for this figure with DMAM
        plt.plot(j,k,color='red')
        rolling_mean = pd.DataFrame(mean_list).rolling(window=5, min_periods=1).mean()  #Calculate DMAM
        plt.plot(j, rolling_mean)
        Moves = 0
        for z in range(PeriodOfTime):                           #TODO Another way for decide Up/Down
            try:
                Moves = Moves + mean_list[z + 1] - mean_list[z]
            except IndexError:
                continue

        if Moves > 0:
            plt.savefig(os.path.join(Deployment_Path, 'Up', j[0] + ' ~ ' + j[PeriodOfTime - 1] + '.jpg'))  # Up
        else:
            plt.savefig(os.path.join(Deployment_Path, 'Down', j[0] + ' ~ ' + j[PeriodOfTime - 1] + '.jpg'))  # Down

        plt.close()



# *****Main Function: this function get full path of .csv file, Method transformation and Period of time for the pictures range*****#
def CreateDataWithGramianAngularField(CsvFilePath, PeriodOfTime, Deployment_Path):
    Close = pd.read_csv(CsvFilePath, usecols=["Close"])
    Open = pd.read_csv(CsvFilePath, usecols=["Open"])
    Date = pd.read_csv(CsvFilePath, usecols=["Date"])
    Open_List = []
    Close_List = []
    Data_List = []

    for row in Open.itertuples(index=True, name='Open'):
        Open_List.append(getattr(row, "Open"))  # Create List of 'Open' data

    for row in Close.itertuples(index=True, name='Close'):
        Close_List.append(getattr(row, "Close"))  # Create List of 'close' data

    for row in Date.itertuples(index=True, name='Date'):
        Data_List.append(getattr(row, "Date"))  # Create List of 'Date' data

    Open_Tuples = tuple(Open_List[i: i + PeriodOfTime] for i in range(0, len(Open), PeriodOfTime - 1))
    Close_Tuples = tuple(Close_List[i: i + PeriodOfTime] for i in range(0, len(Close), PeriodOfTime - 1))
    Date_Tuples = tuple(Data_List[i: i + PeriodOfTime] for i in range(0, len(Date), PeriodOfTime - 1))
    NormalizedData = []
    OriginalData = []
    for i, j, k in zip(Close_Tuples, Date_Tuples, Open_Tuples):
        for x in range(PeriodOfTime):
            try:
                minClose = np.min(i)
                maxClose = np.max(i)
                min_s = np.min(k)
                max_s = np.max(k)
                t = ((i[x] - maxClose) + (i[x] - minClose)) / (maxClose - minClose)     #close
                s = ((k[x] - max_s) + (k[x] - min_s)) / (max_s - min_s) #open
                NormalizedData.append(t)
                OriginalData.append(i[x])
            except IndexError:
                continue
        gaf = GAF()
        g, _, _, _ = gaf(NormalizedData)
        plt.imshow(g, cmap='rainbow', origin='lower')
        plt.axis('off')
        #plt.show()
        Moves = 0
        for z in range(PeriodOfTime):  # TODO Another way for decide Up/Down
            try:
                Moves = Moves + OriginalData[z + 1] - OriginalData[z]
            except IndexError:
                continue

        try:
            if Moves > 0:
                plt.savefig(os.path.join(Deployment_Path, 'Up', j[0] + ' ~ ' + j[PeriodOfTime - 1] + '.jpg'))  # Up
            else:
                plt.savefig(os.path.join(Deployment_Path, 'Down', j[0] + ' ~ ' + j[PeriodOfTime - 1] + '.jpg'))  # Down
        except IndexError:
            break
        NormalizedData.clear()
        OriginalData.clear()
        plt.close()



        # gasf = GramianAngularField( method='summation')
        # X_gasf = gasf.fit_transform(NormalizedData, y=PeriodOfTime)
        # gadf = GramianAngularField(method='difference')
        # X_gadf = gadf.fit_transform(NormalizedData)
        # cnt += 1


        # Show the images for the first time series
        # fig = plt.figure(figsize=(12, 7))
        # grid = ImageGrid(fig, 111,
        #              nrows_ncols=(1, 2),
        #              axes_pad=0.15,
        #              share_all=True,
        #              cbar_location="right",
        #              cbar_mode="single",
        #              cbar_size="7%",
        #              cbar_pad=0.3,
        #              )
        # images = [X_gasf[0] , X_gadf[0]]
        # titles = ['Gramian Angular Summation Field',
        #       'Gramian Angular Difference Field']
        # for image, title, ax in zip(images, titles, grid):
        #     im = ax.imshow(image, cmap='rainbow', origin='lower')
        #     ax.set_title(title)
        # ax.cax.colorbar(im)
        # ax.cax.toggle_label(True)
        # plt.show()

    return


def Main(CsvFileName, Method, PeriodOfTime):
    CsvFilePath = CsvFileName[: len(CsvFileName) - 4:]
    Deployment_Path = Create_Deployment(CsvFilePath)

    if Method == 'Linear Interpolation':
        Linear_Path = os.path.join(Deployment_Path, 'Linear Interpolation')
        Create_Deployment(Linear_Path)
        Create_Deployment(os.path.join(Linear_Path, 'Up'))
        Create_Deployment(os.path.join(Linear_Path, 'Down'))
        CreateDataWithLinearInterpolation(CsvFileName, PeriodOfTime, Linear_Path)

    if Method == 'Moving Average Mapping' or Method == 'MAM':
        MAM_Path = os.path.join(Deployment_Path, 'Moving Average Mapping')
        Create_Deployment(MAM_Path)
        Create_Deployment(os.path.join(MAM_Path, 'Up'))
        Create_Deployment(os.path.join(MAM_Path, 'Down'))
        CreateDataWithMovingAverageMapping(CsvFileName, PeriodOfTime, MAM_Path)

    if Method == 'Double Moving Average Mapping' or Method == 'DMAM':
        DMAM_Path = os.path.join(Deployment_Path, 'Double Moving Average Mapping')
        Create_Deployment(DMAM_Path)
        Create_Deployment(os.path.join(DMAM_Path, 'Up'))
        Create_Deployment(os.path.join(DMAM_Path, 'Down'))
        CreateDataWithDoubleMovingAverageMapping(CsvFileName, PeriodOfTime, DMAM_Path)

    if Method == 'Gramian Angular Field' or 'GAF':
        GAF_Path = os.path.join(Deployment_Path, 'Gramian Angular Field')
        Create_Deployment(GAF_Path)
        Create_Deployment(os.path.join(GAF_Path, 'Up'))
        Create_Deployment(os.path.join(GAF_Path, 'Down'))
        CreateDataWithGramianAngularField(CsvFileName, PeriodOfTime, GAF_Path)





def tabulate(x, y, f):
    """Return a table of f(x, y). Useful for the Gram-like operations."""
    return np.vectorize(f)(*np.meshgrid(x, y, sparse=True))
def cos_sum(a, b):
    """To work with tabulate."""
    return(math.cos(a+b))

class GAF:

    def __init__(self):
        pass
    def __call__(self, serie):
        """Compute the Gramian Angular Field of an image"""
        # Min-Max scaling
        min_ = np.amin(serie)
        max_ = np.amax(serie)
        scaled_serie = (2*serie - max_ - min_)/(max_ - min_)

        # Floating point inaccuracy!
        scaled_serie = np.where(scaled_serie >= 1., 1., scaled_serie)
        scaled_serie = np.where(scaled_serie <= -1., -1., scaled_serie)

        # Polar encoding
        phi = np.arccos(scaled_serie)
        # Note! The computation of r is not necessary
        r = np.linspace(0, 1, len(scaled_serie))

        # GAF Computation (every term of the matrix)
        gaf = tabulate(phi, phi, cos_sum)

        return(gaf, phi, r, scaled_serie)

#Main("Apple Stock Daily - 1.1.2012 ~ 2.4.2019.csv", 'MAM', 10)
#Main("Elbit Stock Daily - 1.1.2012 _ 2.4.2019.csv", 'MAM',10)
#Main("Elbit Stock Daily - 1.1.2012 _ 2.4.2019.csv", 'DMAM',10)

Main("Intel Stock Daily - 1.1.2012 _ 2.4.2019.csv", 'Linear Interpolation',20)
Main("Intel Stock Daily - 1.1.2012 _ 2.4.2019.csv", 'MAM',20)
Main("Intel Stock Daily - 1.1.2012 _ 2.4.2019.csv", 'DMAM',20)
Main("Intel Stock Daily - 1.1.2012 _ 2.4.2019.csv", 'GAF',20)

#Main("Intel Stock Daily - 1.1.2012 _ 2.4.2019.csv", 'MAM',10)
# Main("Apple Stock Daily - 1.1.2012 ~ 2.4.2019.csv", 'Linear Interpolation',10)      #TODO get this value as input from user
