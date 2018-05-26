import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import datetime
import re

#preparing the company dataset for analysis purposes
def clean(company_data):
    company_data.index = pd.to_datetime(company_data.index, errors='coerce')
    company_data.Open = pd.to_numeric(company_data.Open, errors='coerce')
    company_data.High = pd.to_numeric(company_data.High, errors='coerce')
    company_data.Low = pd.to_numeric(company_data.Low, errors='coerce')
    company_data.Close = pd.to_numeric(company_data.Close, errors='coerce')
    company_data.Volume = pd.to_numeric(company_data.Volume, errors='coerce')
    return company_data.sort_index()

#general purpose function to catch integer error
def error_testing(any_input):
    try:
        any_input = int(any_input)
        return(any_input)
    except:
        any_input = "invalid"
        return any_input

#general purpose function for plotting
def plot_data(loop_value, plot_details):
    for i in range(loop_value):
        plt.plot(plot_details[i*2], label = plot_details[i*2 + 1])
    plt.xlabel("Date")          #you may want to stretch the plot window in some case
    plt.ylabel("Closing Price")
    plt.legend(loc = 2)
    plt.show()

# Our programme in terms of what the end user sees starts here.
#we import the data and welcome the user. Optionally we provide some tips and guidelines.
def main():
        try:
            print ("\nDataset is currently loading, please wait.")
            companies_list = pd.read_csv("http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchan0ge=nasdaq&render=download",\
                                      index_col = 0) #index_col=0 treat the first column as the index / read the csv file
            print("\nDear user,\nWelcome to NASDAQ stock exchange.\n\nThis programme aims to provide a user friendly navigation \
that incorporates robust descriptive and predictive features. In order to get the most out if it \
we suggest you spend a bit of time, reading some useful tips. \
If you want to skip this step please enter \'Yes\', otherwise enter \'No\', OR enter \'Exit\' to terminate program.")
            while True:
                skip_intro = input("\nDo you wish to skip this step?")
                if re.match(r'Yes', skip_intro.strip(), re.IGNORECASE):  #Regular experssions (RegEx) have been used to provide an extra level of flexibility
                    company_search(companies_list)
                    break
                elif re.match(r'No', skip_intro.strip(), re.IGNORECASE):
                    print("\nThroughout your navigation in this programme, you can press the \'ENTER\' button once, \
anytime you wish to reload the previous section.\nIf you wish to return to the initial section of this programme, please press the \'ENTER\' button successively, \
until you reach the desired section.")
                    company_search(companies_list)
                    break
                elif re.match(r'Ex', skip_intro.strip(), re.IGNORECASE):
                    print("Programme terminating.")
                    break
                else:
                    print ("Inappropriate input data, please assign a valid value.")
        except:
            print ("Data are currently not available on server.")

# Again in terms of what the user sees, the programme looks up the search input in the companies database, and return matching results
def company_search(companies_list):
    while True:
        company_name = input("\nSearch Company: ")
        if company_name == "":
            company_name = input("Search Company: ")
            if company_name == "":
                print("You assigned a non valid value. Programme terminating.")
                break
        if company_name != "":
            try:
                results = pd.concat([companies_list.Name[companies_list.Name.str.contains(company_name, case=False, na=False)] \
                ,companies_list.Name[companies_list.index.str.contains(company_name, case=False, na=False)]\
                ,companies_list.Name[companies_list.Sector.str.contains(company_name, case=False, na=False)]\
                ,companies_list.Name[companies_list.industry.str.contains(company_name, case=False, na=False)]])    #we are searching similar companies in line with the user input, using regular expresions
                results_verification(results, companies_list)
            except:
                print("Inappropriate input data, please assign a valid value.")

#counting the number of matching results with the user input
def results_verification(results, companies_list):
    if len(results) == 0:
        print("The name that you provided does not exist. Please try again.")
    elif len(results) == 1:
        get_company_data(results.index[0])
    elif len(results) > 1 and len(results) < 21:
        print(results)
        select_company(companies_list)
    else:
        print(results[:20])
        display_more(results[20:], companies_list)
        select_company(companies_list)

# if the user chooses an option that generates more than 20 companies show more!
def display_more(results, companies_list):
    while len(results != 0):
        print("\nThe number of companies generated exceeds the maximum number of entries per page. \
If you wish to see more companies please enter 1, otherwise enter 2 or press Enter.")
        choice = input()
        if choice == "":
            break
        choice = error_testing(choice)
        if choice == 1:
            print(results[:20])
            results = results.drop(results.index[0:20])
        elif choice == 2:
            break
        else:
            print ("Inappropriate input data, please assign a valid value.")

#Selecting one company from the above suggested company names
def select_company(companies_list):
        while True:
            company_symbol = input("\nEnter Company's Symbol: ")
            if company_symbol == "":
                company_symbol = input("Enter Company's Symbol: ")
                if company_symbol == "":
                    break
            if company_symbol.upper() in companies_list.index:
                get_company_data(company_symbol.upper())
            else:
                print("Inappropriate input data, please assign a valid value.")

 #getting the data from the server for the selected company
def get_company_data(company_symbol):
    print("\nData for ", company_symbol, "dataset is currently loading, please wait.")
    try:
        company_data = pd.read_csv("http://finance.google.com/finance/historical?q={}&startdate=Nov+7%2C+2016&enddate=Nov+30%2C+2017&num=30&ei=NGoQWtDQFMGKUIuSsYgF&output=csv".format(company_symbol), index_col = 0)
        #read the data from the csv file (pd.read())
        #index_col=0 treat the first column as the index
        company_data = clean(company_data)
        company_data = change_duration(company_data, company_symbol)
    except:
        print("Data are currently not available on server.")

#checking if the user wants to continue with the default dates, or provide new dates
def change_duration(company_data, company_symbol):
    start_date = (min(company_data.index)).date()
    end_date = (max(company_data.index)).date()
    print("\nData for ", company_symbol, "are available from ", start_date, " up to ", end_date, " (Please note that weekends are not included.)")
    while True:
        print("\nIf you wish to continue with the default dates - please enter 1:")
        print("If you wish to specify new dates               - please enter 2:")
        choice = input()
        if choice == "":
            break
        choice = error_testing(choice)
        if choice == 1:
            analysis_options(company_data)
        elif choice == 2:
            analysis_options(select_dates(company_data))
        else:
            print("Inappropriate input data, please assign a valid value.")

# next step (always in terms of what the user sees) is to define time frame for the required data and relevant company
def select_dates(company_data): #date change is applicable to all statistics
    while True:
        print("\nPlease specify the Start Date (in YYYY-MM-DD format). Please note that weekend days are not valid. \
You may enter \'First\' for the defaul starting date.")
        start_date = input()
        if start_date == "":
            break
        try:
            if start_date.upper() == "FIRST":
                break
            if sum(company_data.index == start_date) == 1:
                start_point_array = company_data.index == start_date
                start_point = np.where(start_point_array == True)[0][0]
                if start_point > 0:
                        company_data = company_data.drop(company_data.index[0:start_point])
                break
            else:
                print("Inappropriate input. Date does not exist.")
        except:
            print("Inappropriate input.")
    while True:
        print("\nPlease specify the End Date (in YYYY-MM-DD format). Please note that weekend days are not valid. \
You may enter \'Last\' for the defaul starting date.")
        end_date = input()
        if end_date == "":
            break
        try:
            if end_date.upper() == "LAST":
                break
            elif sum(company_data.index == end_date) == 1:
                end_point_array = company_data.index == end_date
                end_point = np.where(end_point_array == True)[0][0]
                if end_point < (len(company_data)-1):
                        company_data = company_data.drop(company_data.index[end_point+1:])
                break
            else:
                print ("Inappropriate input data. Date does not exist.")
        except:
            print ("Inappropriate input data, please assign a valid value.")
    return company_data

# at this point we are back in the case where the user has successfully defined a name
# he / she has already been given the choice to choose dates(default or not)
# he / she  has to choose if he/she wishes to view descriptive_statistics, technical indicators or regression analysis
def analysis_options(company_data):
    while True:
        print ("\nIf you wish to select Descriptive Statistics from the analysis menu - please enter 1:")
        print ("If you wish to select Technical Indicators from the analysis menu   - please enter 2:")
        print ("If you wish to select Regression Analysis from the analysis menu    - please enter 3:")
        choice = input()
        if choice == "":
            break
        choice = error_testing(choice)
        if choice == 1:
            descriptive_statistics(company_data)
        elif choice == 2:
            performance_indicator_plots(company_data)
        elif choice == 3:
            prediction(company_data)
        else:
            print ("Inappropriate input data, please assign a valid value.")

# he / she chooses descriptive_statistics
# table with mean, Sample standard deviation, min, max, correlation matrix
def descriptive_statistics(company_data):
    start_date = (min(company_data.index)).date()
    end_date = (max(company_data.index)).date()
    print("\nBelow you will find a quantitative summary of the selected data that are valid from", start_date, " to ", end_date,".","\
    \nIn the first table summary statistics is provided, while on the second you can observe a correlation matrix for the selected data.\n")
    print(company_data.describe())
    print (" ")
    print("Coefficient of Variation:", stats.variation(company_data))
    plt.matshow(company_data.corr())
    plt.xticks(range(len(company_data.columns)), company_data.columns)
    plt.yticks(range(len(company_data.columns)), company_data.columns)
    plt.title("Correlation Matrix\n")
    plt.colorbar()
    plt.show()

# he / she chooses technical indicators
# selection amongst raw time series, trend line, MA, WMA, EMA, MACD
def performance_indicator_plots(company_data):
    while True:
        print ("\nIf you wish to select Raw Time Series Data Visualization                                           - please enter 1:")
        print ("If you wish to fit a Trendline to the selected data                                                - please enter 2:")
        print ("If you wish to visualize the results of the Moving Average over a specific time period             - please enter 3:")
        print ("If you wish to visualize the results of the Weighted Moving Average over a specific time period    - please enter 4:")
        print ("If you wish to visualize the results of the Exponential Moving Average over a specific time period - please enter 5:")
        print ("If you wish to visualize the results of the Moving Average Convergence/Divergence (MACD)           - please enter 6:")
        choice = input()
        if choice == "":
            break
        choice = error_testing(choice)
        if choice == 1:
            time_series(company_data)
        elif choice == 2:
            trend_line(company_data)
        elif choice == 3:
            moving_average(company_data)
        elif choice == 4:
            weighted_moving_average(company_data)
        elif choice == 5:
            exponential_moving_average(company_data)
        elif choice == 6:
            moving_average_convergence_divergence(company_data)
        else:
            print("Inappropriate input data, please assign a valid value.")

#time series function
def time_series(company_data):
    plot_data(1, [company_data.Close, "Raw Time Series"])

#trend line function
def trend_line(company_data):
    date_numeric = pd.to_numeric(company_data.index, errors='coerce')/(10**11)
    line = stats.linregress(date_numeric, company_data.Close)
    trend_value = line[1] + line[0]*date_numeric
    trend_line_dataframe = pd.DataFrame({"Date": company_data.index, "Trend": np.array(trend_value)})
    trend_line_dataframe = trend_line_dataframe.set_index("Date")
    plot_data(2, [company_data.Close, "Raw Time Series", trend_line_dataframe, "Trend Line"])

#moving average function
def moving_average(company_data):
    while True:
        period = input("\nPlease specify input period (in days):")
        if period == "":
            break
        period = error_testing(period)
        if period == "invalid":
            print("Inappropriate input data, please assign a valid value.")
        elif period > 0 and period <= len(company_data):
            moving_average_value = company_data["Close"].rolling(period).mean()
            plot_data(2, [company_data.Close, "Raw Time Series", moving_average_value, "Moving Average" ])
        else:
            print("Inappropriate input data. Value is either above or below limits.")

#weighted moving average function
def weighted_moving_average(company_data):
    while True:
        period = input("\nPlease specify input period (in days):")
        if period == "":
            break
        period = error_testing(period)
        if period == "invalid":
            print("Inappropriate input data, please assign a valid value.")
        elif period > 0 and period <= len(company_data):
            bin_range = company_data.index[period:]
            weights = [(j)/(period*(period+1)/2) for j in range(1,period+1)]    #currently using default weights
            moving_averages = [sum(company_data.Close[i: period + i]*weights) for i in range(len(company_data) - period)]
            weighted_moving_averages = pd.DataFrame({"Date": bin_range, "Moving Average": np.array(moving_averages)})
            weighted_moving_averages = weighted_moving_averages.set_index("Date")
            plot_data(2, [company_data.Close, "Raw Time Series", weighted_moving_averages, "Weighted Moving Average" ])
        else:
            print("Inappropriate input data. Value is either above or below limits.")

#exponential moving average function
def exponential_moving_average(company_data):
    while True:
        period = input("\nPlease specify input period:")
        if period == "":
            break
        period = error_testing(period)
        if period == "invalid":
            print ("Inappropriate input data, please assign a valid value.")
        elif period > 0 and period <= len(company_data):
            exponential_moving_averages = company_data["Close"].ewm(span = period).mean()
            plot_data(2, [company_data.Close, "Raw Time-series", exponential_moving_averages, "Exponential Moving Average" ])
        else:
            print("Inappropriate input data. Value is either above or below limits.")

#moving average convergence divergence function
def moving_average_convergence_divergence(company_data):
    ema26 = company_data["Close"].ewm(span = 26).mean()
    ema12 = company_data["Close"].ewm(span = 12).mean()
    macd_value = ema12 - ema26
    signal = macd_value.ewm(span = 9).mean()
    crossover = macd_value - signal
    f, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    ax1.plot(company_data.Close)
    ax1.set_title('Raw Time Series')
    ax1.set_ylabel('Closing Price')
    ax2.plot(macd_value, label = "Moving Average Convergence/Divergence")
    ax2.plot(signal, label = "Signal")
    ax2.plot(crossover, label = "Crossover")
    plt.legend(loc = 2)
    plt.show()

# he / she chooses polynomial regression for prediction
# needs to specify input period
def prediction(company_data):
    deg = 3 #Currently a cubic polynomial
    date_numeric = pd.to_numeric(company_data.index, errors='coerce')/(10**11)
    decision_variables = np.polyfit(date_numeric, company_data.Close, deg)
    decision_variables = decision_variables[::-1]
    while True:
        period = input("\nPlease specify input period in days (maximum limit 10 days):")    #This is currently set to 10
        if period == "":
            break
        period = error_testing(period)
        if period == "invalid":
            print ("Inappropriate input data, please assign a valid value.")
        elif period > 0 and period < 11:
            prediction_dates = pd.date_range(start=max(company_data.index).date() + datetime.timedelta(days=1), periods = period, freq='B') #adding the number of weekdays which the user has defined before
            prediction_date_numeric = pd.to_numeric(prediction_dates, errors='coerce') / (10**11) #converting timestamps into date values, and then dividing it by 10^11 to remove additional zeroes. Otherwise scalar errors
            close_new = decision_variables[0] + sum((decision_variables[i]*(date_numeric.append(prediction_date_numeric)**i)) for i in range (1,deg+1)) #adding the prediction dates to the existing dates, and calculating the predicted closing prices
            close_new = close_new[close_new > 0]
            bin_range = company_data.index.append(prediction_dates)[:len(close_new)]
            prediction_dataframe = pd.DataFrame({"Date": bin_range, "Prediction": np.array(close_new)})
            prediction_dataframe = prediction_dataframe.set_index("Date")
            print("Predictions:\n", prediction_dataframe[-period:])
            plot_data(2, [company_data.Close, "Raw Time Series", prediction_dataframe, "Prediction Line" ])
        else:
            print ("Inappropriate input data. Value is either above or below limits.\n")

#this is the line that initializes the programme
if __name__ == "__main__":
    main()
