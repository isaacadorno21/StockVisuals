import sys
import requests
import ftplib
import matplotlib.pyplot as plt
import numpy as np

# Plan to use Alpha Vantage to grab "realtime and historical" stock data
# Plan to use Dash and Pandas for data visualization in the future

def main():
    # TEXT Introduction
    # Good to start but eventually I want a full GUI!
    print("--------------------")
    print("STOCK VISUALIZER")
    print("--------------------")
    stock = input("Enter the ticker of a share to get into: ").upper()

    company_info = getCompanyBasicInfo(stock)
    if company_info == "N/A":
        print("Stock does not exist. Program terminating....")
        sys.exit()

    printCompanyBasicInfo(company_info)

    apiKey = getKey()
    print("List of Available Functions:")
    print("TIME_SERIES_INTRADAY: intraday time series (timestamp, open, high, low, close, volume)")
    print("TIME_SERIES_DAILY:  daily time series (date, daily open, daily high, daily low, daily close, daily volume)")
    print("TIME_SERIES_DAILY_ADJUSTED: daily time series (date, daily open, daily high, daily low, daily close, daily volume, daily adjusted close, and split/dividend events)")
    print("TIME_SERIES_WEEKLY: weekly time series (last trading day of each week, weekly open, weekly high, weekly low, weekly close, weekly volume)")
    print("TIME_SERIES_WEEKLY_ADJUSTED: weekly adjusted time series (last trading day of each week, weekly open, weekly high, weekly low, weekly close, weekly adjusted close, weekly volume, weekly dividend)")
    print("TIME_SERIES_MONTHLY: monthly time series (last trading day of each month, monthly open, monthly high, monthly low, monthly close, monthly volume)")
    print("TIME_SERIES_MONTHLY_ADJUSTED: monthly adjusted time series (last trading day of each month, monthly open, monthly high, monthly low, monthly close, monthly adjusted close, monthly volume, monthly dividend)")
    print("GLOBAL_QUOTE: the latest price and volume information")
    print("")
    function = input("Enter the wanted function: ")

    query = 'https://www.alphavantage.co/query?function=' + function + '&symbol=' + stock + '&apikey=' + apiKey
    r = requests.get(query)
    displayGraph(r.json(), function, company_info[1])


def getKey():
    configFile = open("APIConfig.txt", "r")
    if configFile.mode == 'r':
        return configFile.read()
    else:
        print("Proper API Key not found. Program terminating....")
        sys.exit()


def getCompanyBasicInfo(stock):
    # Get's company name from NASDAQ, NYSE, other exchanges

    nasdaq_file = 'nasdaqlisted.txt'
    other_file = 'otherlisted.txt'

    ftp_srv = 'ftp.nasdaqtrader.com'
    ftp = ftplib.FTP(ftp_srv)
    ftp.login()
    ftp.cwd('SymbolDirectory')

    local_nasdaq_dir = 'data/nasdaqlisted.txt'
    local_nasdaq_file = open(local_nasdaq_dir, 'wb')
    ftp.retrbinary('RETR ' + nasdaq_file, local_nasdaq_file.write, 1024)

    local_other_dir = 'data/otherlisted.txt'
    local_other_file = open(local_other_dir, 'wb')
    ftp.retrbinary('RETR ' + other_file, local_other_file.write, 1024)

    ftp.quit()
    local_nasdaq_file.close()
    local_other_file.close()

    local_nasdaq_file = open(local_nasdaq_dir, "r+")
    for line in local_nasdaq_file:
        cur_line = line.split("|")
        if cur_line[0] == stock:
            local_nasdaq_file.truncate(0)
            local_nasdaq_file.close()
            open(local_other_dir, 'w').close()
            return cur_line
    local_nasdaq_file.truncate(0)
    local_nasdaq_file.close()

    # If we get to this point, the company wasn't listed under the NASDAQ exchange
    local_other_file = open(local_other_dir, "r+")
    for line in local_other_file:
        cur_line = line.split("|")
        if cur_line[0] == stock:
            local_other_file.truncate(0)
            local_other_file.close()
            return cur_line
    local_other_file.truncate(0)
    local_other_file.close()
    return "N/A"


def printCompanyBasicInfo(company_info):
    # Print out basic info about the company,

    print("--------------------")
    print("Ticker Symbol: " + company_info[0])
    print("Company Name: " + company_info[1])
    market_category = ""
    if company_info[2] == "Q":
        market_category = "NASDAQ Global Select MarketSM"
    elif company_info[2] == "G":
        market_category = "NASDAQ Global MarketSM"
    elif company_info[2] == "S":
        market_category = "NASDAQ Capital Market"
    print("Market Category: " + market_category)
    test_issue = "Yes" if company_info[3] == "Y" else "No"
    print("Test Issue: " + test_issue)
    financial_status = ""
    if company_info[4] == "D":
        financial_status = "Deficient"
    elif company_info[4] == "E":
        financial_status = "Delinquent"
    elif company_info[4] == "Q":
        financial_status = "Bankrupt"
    elif company_info[4] == "N":
        financial_status = "Normal"
    elif company_info[4] == "G":
        financial_status = "Deficient and Bankrupt"
    elif company_info[4] == "H":
        financial_status = "Deficient and Delinquent"
    elif company_info[4] == "J":
        financial_status = "Delinquent and Bankrupt"
    elif company_info[4] == "K":
        financial_status = "Deficient, Delinquent, and Bankrupt"
    print("Financial Status: " + financial_status)
    print("Round Lot Size: " + company_info[5])
    print("--------------------")

def displayGraph(company_data, function, company_name):
    date_list = np.linspace(start=1, stop=100, num=100)
    daily_list = []
    function_label = ""
    data_point_type = ""

    if function == "TIME_SERIES_DAILY":
        function_label = 'Time Series (Daily)'
        print("--------------------")
        print("List of Available Data Points:")
        print("1. open")
        print("2. high")
        print("3. low")
        print("4. close")
        print("5. volume")
        print("")

    data_point_type = input("Enter the type of data you'd like to view: ")

    for value in company_data[function_label].values():
        daily_list.append(float(value[data_point_type]))

    plt.plot(date_list, daily_list)
    plt.ylabel('Daily Open')
    plt.xlabel('Days')
    plt.title(company_name)
    plt.axis([0, 100, min(daily_list) * 0.9, max(daily_list) * 1.1])
    plt.show()

main()


# To Do:
# Add base cases and edge cases
# Add status codes to requests
# Refactor :o
# Use Alpha Vantage Search Endpoint instead of FTP
# Remove hardcoding
