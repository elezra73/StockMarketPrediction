import pandas as pd
from datetime import datetime
from matplotlib import pyplot as plt

def UserSelectPredict(Stock,Model,DateFrom,DateTo):
    '''
            first, check if the 'DateTo' is a future date -> predict
                otherwise, get this data from .csv file
           '''



    Close = pd.read_csv(Stock, usecols=["Close"])
    Date = pd.read_csv(Stock, usecols=["Date"])

    Close_List = []
    Date_List = []
    for row in Close.itertuples(index=True, name='Close'):
        Close_List.append(getattr(row, "Close"))  # Create List of 'close' data

    for row in Date.itertuples(index=True, name='Date'):
        Date_List.append(getattr(row, "Date"))  # Create List of 'close' data

    last_date = Date_List[-1]

    DateFrom

    input_fromDate = datetime(int('20' + DateFrom[6::1]), int(DateFrom[3:5:1]), int(DateFrom[0:2:1]))
    input_toDate = datetime(int('20' + DateTo[6::1]), int(DateTo[3:5:1]), int(DateTo[0:2:1]))
    #current_date = datetime(int(datetime.now().date().year), int(datetime.now().date().month), datetime.now().date().day)
    last_date_from_db = datetime(int('20' + last_date[6::1]), int(last_date[3:5:1]), int(last_date[0:2:1]))




    if input_toDate > last_date_from_db:            #Prediction case
        print('Prediction')

        #TODO here we need to call the model to predict movements



    else:
        days = (input_toDate - input_fromDate).days
        print('from data. ' + 'Total for calculation is: ' + str(days) + ' days')


        try:
            start_index = Date_List.index(DateFrom)
            end_index = Date_List.index(DateTo)
        except:
            print('this days has no trades')
            exit(1)


        actual_date = []
        actual_close = []

        for x in range (start_index,end_index):
            actual_date.append(Date_List.__getitem__(x))
            actual_close.append(Close_List.__getitem__(x))



        plt.plot(legend=None)
        # plt.axis('off')
        plt.plot(actual_date, actual_close)
        #plt.savefig(os.path.join(Deployment_Path, j[0] + ' ~ ' + j[PeriodOfTime - 1]))
        plt.show()
        return(plt)





UserSelectPredict(Stock='Apple Stock Daily - 1.1.2012 ~ 2.4.2019.csv',Model=0,DateFrom='09-01-13',DateTo='17-01-14')




#def UserSelectTraining

#def UserSelectPredictionTest

