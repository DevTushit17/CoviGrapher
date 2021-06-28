import urllib.request as ur
from pandas import Series, read_csv
from matplotlib.pyplot import plot, xticks, show, title, xlabel, ylabel, savefig
from datetime import datetime, timedelta
import os


def covigrapher():
    data = None
    
    # source of data
    link = "https://api.covid19india.org/csv/latest/districts.csv"

    # checking weather file exists
    if os.path.isfile("CovidData.csv"):
        
        #data from .csv file is read to Dataframe to use data in graphs
        data = read_csv("CovidData.csv")

        currentDate = datetime.today()
        currentDate = currentDate.date()

        print("[Info] Data file is present")
        lastDate = data.tail()['Date'].iloc[-1]
        lastDate = datetime.strptime(lastDate, "%Y-%m-%d")
        lastDate = lastDate.date()
        print(lastDate)
        print(currentDate)
        delta = timedelta(1)
        print(currentDate - delta)

        # checking weather data is up-to-date
        if lastDate == currentDate:
            print("[Info] Data is up-to-date ")
            pass
        # data is updated by evening, so sometimes lastDate is not equivalent to currentDate 
        elif lastDate == (currentDate - delta):
            print("[Info] Data is up-to-date ")
            pass 

        # if data is not up-to-date, data file is deleted and re-downloaded
        else:
            os.remove("CovidData.csv")
            
            print("[Info] Data is not up-to-date")
            
            print("Updating Data, please wait...")
            link = "https://api.covid19india.org/csv/latest/districts.csv"
            ur.urlretrieve(link, "CovidData.csv")
            data = read_csv("CovidData.csv")
            print("Updating complete")

    # if file doesn't exist then the file is downloaded
    else:
        print("[Info] Data file is not present")
        print("Data not found, downloading data, please wait...")
        ur.urlretrieve(link, "CovidData.csv")
        data = read_csv("CovidData.csv")

    statusSeries = Series({1: "Confirmed", 2: "Active", 3: "Recovered", 4: "Deceased"})

    #The active cases can be calculated by the following method.
    data['Active'] = (data['Confirmed'] - (data['Recovered'] + data['Deceased']))

    #Asking the name of city for the graph.
    district = str(input("Enter the name of the city : "))
    print("Enter the number corresponding to the data you want to view the graph of : ")
    print(statusSeries.to_string())
    datatype = int(input("Enter the number corresponding to the data you want to see : "))

    #Getting the x and y values based on the input
    #[Refer to the downloaded .csv file for the column names]
    xValues = data[data['District'] == district]['Date']
    yValues = data[data['District'] == district][statusSeries[datatype]]

    # plotting the graph
    plot(xValues, yValues, color="blue")
    xlabel(f"From {xValues.iloc[1]} to {xValues.iloc[-1]}")
    ylabel("Number of cases")
    title(f"Graph of {statusSeries[datatype]} cases of the {district} district.")
    xticks(ticks=" ")
    show()


covigrapher()

rerun = 1
while rerun == 1:
    rerun = int(input("Enter 1 if you want to run the program again, 0 if you want to close it : "))
    if rerun == 1:
        covigrapher()
    elif rerun == 0:
        print("Thanks for using.")
        quit()
    else:
        print("Invalid Response")
