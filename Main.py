import sys
#import json
import requests
import ftplib

# Plan to use Alpha Vantage to grab "realtime and historical" stock data
# Plan to use Dash and Pandas for data visualization in the future


def main():
    print(sys.executable)
    # TEXT Introduction
    # Good to start but eventually I want a full GUI!
    print("--------------------")
    print("STOCK VISUALIZER")
    print("--------------------")
    stock = input("Enter the ticker of a share to get into: ")
    apiKey = getKey()
    testQuery = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + stock + '&apikey=' + apiKey
    r = requests.get(testQuery)

    company_info = getCompanyBasicInfo(stock)
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
    print(r.text)


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

    local_filedir = 'data/nasdaqlisted.txt'
    localfile = open(local_filedir, 'wb')
    ftp.retrbinary('RETR ' + nasdaq_file, localfile.write, 1024)

    ftp.quit()
    localfile.close()

    localfile = open(local_filedir, "r")
    for line in localfile:
        cur_line = line.split("|")
        if cur_line[0] == stock:
            return cur_line

main()


# To Do:
# Clear file when done OR check if file needs to be written - diff FTP file and local
# Actually use data instead of just printing out
# Add base cases and edge cases
# Refactor :o
