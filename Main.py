import sys
#import json
import requests

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

def getKey():
    configFile = open("APIConfig.txt", "r")
    if (configFile.mode == 'r'):
        return configFile.read()
    else:
        print("Proper API Key not found. Program terminating....")
        sys.exit()

main()
