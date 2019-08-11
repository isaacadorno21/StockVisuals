import sys
#import json
import requests
import ftplib

# Plan to use Alpha Vantage to grab "realtime and historical" stock data
# Plan to use Dash and Pandas for data visualization in the future

def main():

    print(sys.executable)
    #TEXT Introduction
    #Good to start but eventually I want a full GUI!
    print("--------------------")
    print("STOCK VISUALIZER")
    print("--------------------")
    stock = input("Enter the ticker of a share to get into: ")
    apiKey = getKey()
    testQuery = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=' + stock + '&interval=60min&apikey=' + apiKey
    r = requests.get(testQuery)
    print(r.text)
    getCompanyName(stock)

def getKey():
    configFile = open("APIConfig.txt", "r")
    if (configFile.mode == 'r'):
        return configFile.read()
    else:
        print("Proper API Key not found. Program terminating....")
        sys.exit()

def getCompanyName(stock): #Get's company name from NASDAQ, NYSE, other exchanges
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

    with open(local_filedir, 'r') as fin:
        print(fin.read())

main()

##To Do:
# Clear file when done OR check if file needs to be written - diff FTP file and local
# Actually use data instead of just printing out