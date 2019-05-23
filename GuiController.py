import pandas as pd
from datetime import datetime,timedelta
from matplotlib import pyplot as plt

def ParseStringToPlotDate(String):
    return String[8:10:1] + '-' + String[5:7:1]

def ParseStringToDate(String):
    return datetime(int(String[:4:1]), int(String[5:7:1]), int(String[8:10:1])).date()

def ParseDateToString(Date):
    s = Date.strftime("%Y-%m-%d %H:%M:%S")
    return s[0:4:1] + '-' + s[5:7:1] + '-' + s[8:10:1]

def GetTradingDates(Date_List,DateFrom,DateTo):

    while DateFrom not in Date_List:                 #look for next valid trading day
        input_FromDate = ParseStringToDate(DateFrom)
        DateFrom = ParseDateToString(input_FromDate + timedelta(days=1))

    while DateTo not in Date_List:                  #look for pervious valid trading day
        input_toDate = ParseStringToDate(DateTo)
        DateTo = ParseDateToString(input_toDate + timedelta(days=-1))

    return Date_List.index(DateFrom), Date_List.index(DateTo)       #return the index of the required tranding dates

def UserSelectPredict(Stock, StartDateForPrediction, EndDateForPrediction):
    Close = pd.read_csv(Stock, usecols=["Close"])
    Date = pd.read_csv(Stock, usecols=["Date"])
    Close_List = []
    Date_List = []

    for row in Close.itertuples(index=True, name='Close'):
        Close_List.append(getattr(row, "Close"))  # Create List of 'close' data

    for row in Date.itertuples(index=True, name='Date'):
        Date_List.append(getattr(row, "Date"))  # Create List of 'close' data

    FirstDateFromCsvFile = Date_List[0]
    LastDateFromCsvFile = Date_List[-1]

    StartDate = ParseStringToDate(StartDateForPrediction)
    EndDate = ParseStringToDate(EndDateForPrediction)
    #current_date = datetime(int(datetime.now().date().year), int(datetime.now().date().month), datetime.now().date().day)
    first_date_from_csv = ParseStringToDate(FirstDateFromCsvFile)
    last_date_from_csv = ParseStringToDate(LastDateFromCsvFile)

    if StartDate < first_date_from_csv:
        print('You choose an old date, this information does not exist')
        return

    if EndDate > last_date_from_csv:            #Prediction case
        print('Prediction')

        #TODO here we need to call the model to predict movements


def UserSelectHistoricalData(Stock, StartDateForPrediction, EndDateForPrediction):
    Close = pd.read_csv(Stock, usecols=["Close"])
    Date = pd.read_csv(Stock, usecols=["Date"])
    Close_List = []
    Date_List = []

    for row in Close.itertuples(index=True, name='Close'):
        Close_List.append(getattr(row, "Close"))  # Create List of 'close' data

    for row in Date.itertuples(index=True, name='Date'):
        Date_List.append(getattr(row, "Date"))  # Create List of 'close' data

    start_index, end_index = GetTradingDates(Date_List, StartDateForPrediction, EndDateForPrediction)
    actual_date = []
    actual_close = []

    for x in range(start_index, end_index):
        actual_date.append(ParseStringToPlotDate(Date_List.__getitem__(x)))
        actual_close.append(Close_List.__getitem__(x))

    RollingMeanWeek = pd.DataFrame(actual_close).rolling(window=5).mean()
    RollingMeanTwoWeek = pd.DataFrame(actual_close).rolling(window=10).mean()

    if actual_close[0] <= actual_close[-1]:
        plt.plot(actual_date, actual_close, label=str(Stock[: len(Stock) - 4:] + ' Daily'))
        plt.plot(actual_date, RollingMeanWeek, label=str(Stock[: len(Stock) - 4:] + ' 7 Days MAM'))
        plt.plot(actual_date, RollingMeanTwoWeek, label=str(Stock[: len(Stock) - 4:] + ' 14 Days MAM'))
        plt.xticks(rotation=-45)
    else:
        plt.plot(actual_date, actual_close, label=str(Stock[: len(Stock) - 4:] + ' Daily'))
        plt.plot(actual_date, RollingMeanWeek, label=str(Stock[: len(Stock) - 4:] + ' 7 Days MAM'))
        plt.plot(actual_date, RollingMeanTwoWeek, label=str(Stock[: len(Stock) - 4:] + ' 14 Days MAM'))
        plt.xticks(rotation=-45)
    plt.legend(loc='upper left')
    #plt.savefig('C:\\Users\\Daniel\\Desktop\\t.png')       #TODO Avner save this fig and return the ImgPath
    plt.show()
    return plt  # after create the Figure, send it to the server





'''Call UserSelectPredict function '''
#UserSelectPredict(Stock='Apple Stock Daily - 1.1.2012 ~ 2.4.2019.csv', Model=0, StartDateForPrediction='09-05-12', EndDateForPrediction='20-05-12')

UserSelectHistoricalData(Stock='AAPL.csv', StartDateForPrediction='2018-06-07', EndDateForPrediction='2018-07-21')

UserSelectPredict(Stock='AAPL.csv', Model=0, StartDateForPrediction='2019-05-07', EndDateForPrediction='2019-05-21')
