import pandas as pd
from datetime import datetime,timedelta
from matplotlib import pyplot as plt


def ParseStringToDate(String):
    return datetime(int('20' + String[6::1]), int(String[3:5:1]), int(String[0:2:1]))

def ParseDateToString(Date):
    s = Date.strftime("%Y-%m-%d %H:%M:%S")
    return s[8:10:1] + '-' + s[5:7:1] + '-' + s[2:4:1]

def GetTradingDates(Date_List,DateFrom,DateTo):

    while DateFrom not in Date_List:                 #look for next valid trading day
        input_FromDate = ParseStringToDate(DateFrom)
        DateFrom = ParseDateToString(input_FromDate + timedelta(days=1))

    while DateTo not in Date_List:                  #look for pervious valid trading day
        input_toDate = ParseStringToDate(DateTo)
        DateTo = ParseDateToString(input_toDate + timedelta(days=-1))

    return Date_List.index(DateFrom), Date_List.index(DateTo)       #return the index of the required tranding dates

def UserSelectPredict(Stock, Model, StartDateForPrediction, EndDateForPrediction):
    ''' first, check if the 'StartDateForPrediction' is a future date -> predict
                otherwise, get this data from .csv file if this data exist '''

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

    else:
        days = (EndDate - StartDate).days
        print('from data. ' + 'Total for calculation is: ' + str(days) + ' days')


        start_index, end_index = GetTradingDates(Date_List, StartDateForPrediction, EndDateForPrediction)
        actual_date = []
        actual_close = []

        for x in range(start_index,end_index):
            actual_date.append(Date_List.__getitem__(x))
            actual_close.append(Close_List.__getitem__(x))

        #
        if actual_close[0] <= actual_close[-1]:
            plt.plot(actual_date, actual_close,label=str(int(actual_close[-1] - actual_close[0])) + ' profit')
        else:
            plt.plot(actual_date, actual_close, label=str(round(float(actual_close[-1] - actual_close[0]))) + ' Negative')
        plt.legend(loc='upper left')
        #plt.savefig(os.path.join(Deployment_Path, j[0] + ' ~ ' + j[PeriodOfTime - 1]))
        plt.show()
        return plt      #after create the Figure, send it to the server

'''Call UserSelectPredict function '''
UserSelectPredict(Stock='Apple Stock Daily - 1.1.2012 ~ 2.4.2019.csv', Model=0, StartDateForPrediction='09-05-12', EndDateForPrediction='20-05-12')


#def AdminSelectTraining

#def AdminSelectPredictionTest

