import csv
import json
import os
import matplotlib.pyplot as plt
import numpy
import numpy as np
import pandas as pd
import reverse_geocoder as rg
import datetime
from datetime import datetime
from dateutil import parser

from dateutil.parser import parse

from RetrieveAddress import RetrieveAddress


class ReadContent():
    def __init__(self, fileAddress):
        self.fileAddress = fileAddress
        self.header = []
        self.rows = []
        fileName = self.fileAddress.split('/')[-1].split('.')[0]

        # checks if the format is CSV
        if fileAddress.split('.')[-1].lower() == "csv":
            file = open(self.fileAddress)
            csvReader = csv.reader(file)

            # generates headers and rows lists
            self.header = next(csvReader)
            for row in csvReader:
                self.rows.append(row)
            file.close()

        # if format is not CSV, creates a new CSV file
        elif fileAddress.split('.')[-1].lower() == "txt":

            JSONObjects = []
            with open(self.fileAddress) as f:
                for jsonObj in f:
                    tempDict = json.loads(jsonObj)
                    JSONObjects.append(tempDict)

            # headers of the new CSV file that is going to be generated from JSON objects
            self.header.append("TIMESTAMP")
            self.header.append(fileName)

            # rows of the new CSV file that is going to be generated from JSON objects
            for obj in JSONObjects:
                for item in obj:
                    tempList = [item, obj[item]]
                    self.rows.append(tempList)

            # creating address for the new CSV file to be written
            self.writeNewCSVFile(self.header, self.rows)

        # elif fileAddress.split('.')[-1].lower() == "ttl":

    def getFirstRow(self):
        return self.rows[0]

    def getLastRow(self):
        return self.rows[-1]

    def getHeaders(self):
        return self.header

    # returns number of rows in CSV formatted file
    def getSize(self):
        return len(self.rows)

    @staticmethod
    def getFileFormat(fileAddress):
        return fileAddress.split('.')[-1].lower()

    def writeNewCSVFile(self, headers, rows):
        if self.getFileFormat(self.fileAddress) == 'csv':
            pathToWriteCSV = self.fileAddress
        else:
            my_path = os.path.abspath(os.path.dirname(__file__)) + "/input files/"
            temp = self.fileAddress.split("/")[-1].split(".")[0] + ".csv"
            pathToWriteCSV = os.path.join(my_path, temp)
        with open(pathToWriteCSV, 'w') as file:
            write = csv.writer(file)
            write.writerow(headers)
            write.writerows(rows)
        file.close()

    @staticmethod
    def isValidDate(string, fuzzy=False):
        try:
            parse(string, fuzzy=fuzzy)
            return True
        except ValueError:
            return False

    def getMaxValueOfColumn(self, columnName):
        if columnName in self.header:
            tempList = []
            max([], default="EMPTY")
            index = self.header.index(columnName)
            for row in self.rows:
                try:
                    tempList.append(int(row[index]))
                except:
                    continue
            return max(tempList)

    def getMinValueOfColumn(self, columnName):
        if columnName in self.header:
            tempList = []
            min([], default="EMPTY")
            index = self.header.index(columnName)
            for row in self.rows:
                try:
                    tempList.append(int(row[index]))
                except:
                    continue
            return min(tempList)

    def getAvgValueOfColumn(self, columnName):
        if columnName in self.header:
            tempList = []
            index = self.header.index(columnName)
            for row in self.rows:
                try:
                    tempList.append(int(row[index]))
                except:
                    continue

            npArr = numpy.array(tempList)
            return numpy.mean(npArr)

    @staticmethod
    def checkTypeOfVariable(var, typeOfVar):
        try:
            if isinstance(var, typeOfVar):
                return True
            else:
                return False
        except:
            return False

    def plotFromBarChartForOneCSV(self, *args):

        intColumns = []
        if len(args) == 0:
            for item in self.rows[0]:
                try:
                    int(item)
                    intColumns.append(self.rows[0].index(item))
                except:
                    continue
        else:
            for item in args:
                if item in self.header:
                    intColumns.append(self.header.index(item))
            if len(intColumns) == 0:
                return

        barsList = []
        for item in intColumns:
            barsList.append(self.header[item])

        heights = []
        for item in barsList:
            heights.append(self.getAvgValueOfColumn(item))
            print(self.getAvgValueOfColumn(item))

        bars = tuple(barsList)
        y_pos = numpy.arange(len(bars))
        plt.subplots_adjust(left=0.1, bottom=0.25, right=0.9, top=0.9)

        # Create bars
        plt.bar(y_pos, heights, width=0.5)

        # Create names on the x-axis
        plt.xticks(y_pos, bars, rotation=45)

        plt.show()

    @staticmethod
    def reverseGeocode(long, lat):
        coordinates = (long, lat)
        print(rg.search(coordinates), "\n")

    def createFormattedAddressColumn(self):
        locationHeaders = ["latitude", "longitude", "location", "address"]
        indexesList = []
        for item in locationHeaders:
            if item.lower() in self.header:
                indexesList.append(self.header.index(item))

        retrieveAddress = RetrieveAddress()

        if len(indexesList) == 0 or "Formatted Address" in self.header:
            return
        else:
            self.header.append("Formatted Address")
            address = ""
            for row in self.rows:
                for item in indexesList:
                    address += " " + row[item]
                row.append(retrieveAddress.getFormattedAddress(address))
                address = ""

        self.writeNewCSVFile(self.header, self.rows)

    @staticmethod
    def plotLineChart(firstFile, secondFile, *yLabels):
        files = []
        plotDict = dict()

        for file in [firstFile, secondFile]:
            if '\\' not in file:
                my_path = os.path.abspath(os.path.dirname(__file__)) + "/input files/" + file
                files.append(my_path)
            elif '\\' in file:
                files.append(file)

        for file in files:
            rows = []
            fh = open(file)
            csvReader = csv.reader(fh)

            # generates headers and rows lists
            header = next(csvReader)
            for row in csvReader:
                rows.append(row)
            for item in header:
                header[header.index(item)] = item.lower()
            timeStampIndex = header.index("timestamp")

            for item in yLabels:
                if item.lower() in header:
                    rowIndex = header.index(item.lower())
                    timeStamps = []
                    for row in rows:
                        plotDict[row[timeStampIndex]] = row[rowIndex]
                        timeStamps.append(row[timeStampIndex])

                    Xs = []
                    Ys = []

                    for elem in plotDict:
                        Xs.append(elem)
                        Ys.append(int(plotDict[elem]))

                    const = float(100 / len(Xs))
                    temp = 0

                    for x in Xs:
                        Xs[Xs.index(x)] = temp * const
                        temp += 1
                    plotDict.clear()

                    plt.figure(figsize=(15, 9))
                    plt.plot(Xs, Ys)
                    plt.title(file)
                    plt.xlabel("time")
                    plt.ylabel(item)
                    a = []
                    b = []
                    for i in range(0, 100, 10):
                        a.append(i)
                        b.append(timeStamps[int(len(timeStamps) * i / 100)])
                    plt.xticks(a, b, rotation=45)

                    plt.show()

            # for item in xValues:
            #     if 'T' not in item:
            #         temp = item.split(' ')
            #         xValues[xValues.index(item)] = temp[0] + 'T' + temp[1]
            #
            # dates = [datetime.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S") for ts in xValues]
            # dates.sort()
            # sortedDates = ([datetime.datetime.strftime(ts, "%Y-%m-%dT%H:%M:%S") for ts in dates])
            # for item in sortedDates:
            #     finalXValues.append(item)
            # finalXValues = list(dict.fromkeys(finalXValues))

            fh.close()

    @staticmethod
    def plotOneLineChartFromMultipleFiles(filesList, headersList):
        files = []
        plotDict = dict()
        timestamps = []
        dateTimeFormat = "%Y-%m-%dT%H:%M:%S"

        for file in filesList:
            if '\\' not in file:
                my_path = os.path.abspath(os.path.dirname(__file__)) + "/input files/" + file
                files.append(my_path)
            elif '\\' in file:
                files.append(file)

        allXs = []
        allYs = []
        for file in files:
            rows = []
            fh = open(file)
            csvReader = csv.reader(fh)

            # generates headers and rows lists
            header = next(csvReader)
            for item in header:
                header[header.index(item)] = item.lower()
            for row in csvReader:
                rows.append(row)

            if "timestamp" in header:
                index = header.index("timestamp")
                for row in rows:
                    if 'T' not in row[index]:
                        temp = row[index].split(' ')
                        row[index] = temp[0] + 'T' + temp[1]
                        timestamps.append(row[index])
                    elif 'T' in row[index]:
                        timestamps.append(row[index])
            timestamps = list(dict.fromkeys(timestamps))
            # dates = [datetime.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S") for ts in timestamps]
            # dates.sort()
            # sortedDates = ([datetime.datetime.strftime(ts, "%Y-%m-%dT%H:%M:%S") for ts in dates])

            for item in headersList:
                item = item.lower()
                if item in header and "timestamp" in header:
                    tempXs = []
                    tempYs = []
                    for row in rows:
                        if 'T' not in row[header.index('timestamp')]:
                            temp = row[header.index('timestamp')].split(' ')
                            row[header.index('timestamp')] = temp[0] + 'T' + temp[1]
                            tempXs.append(row[header.index('timestamp')])
                        elif 'T' in row[header.index('timestamp')]:
                            tempXs.append(row[header.index('timestamp')])
                        tempYs.append(row[header.index(item)])
                    allXs.append(tempXs)
                    allYs.append(tempYs)

        plt.figure(figsize=(15, 9))
        i = 0
        for i in range(0, len(allXs)):
            for item in allXs[i]:
                allXs[i][allXs[i].index(item)] = timestamps.index(item)
            # print(allXs)
            for j in range(0, len(allYs[i])):
                allYs[i][j] = float(allYs[i][j])
                if not isinstance(allYs[i][j], float):
                    print("error")
            plt.plot(allXs[i], allYs[i])


        plt.xlabel('x - axis')
        plt.ylabel('y - axis')
        # a = []
        # b = []
        # for i in range(0, 100, 10):
        #     b.append(timestamps[int(len(timestamps) * i / 100)])
        # plt.xticks(a, b, rotation=45)
        plt.show()

    @staticmethod
    def plotPandas(filesList):

        file = "/home/amirhossein/Documents/GitHub/new-temp/input files/pollutionData158324.csv"
        fh = open(file)
        csvReader = csv.reader(fh)
        # generates headers and rows lists
        headers = next(csvReader)

        df = pd.read_csv(file, names=headers)

        # df['timestamp'] = df['timestamp'].map(lambda x: datetime.strptime(str(x), "%Y-%m-%d %H:%M:%S"))
        x = df['timestamp']
        y = df["carbon_monoxide"]

        finalYs = []
        finalXs = []

        for i in range(1, len(x)):
            finalXs.append(x[i])
        for item in y:
            try:
                finalYs.append(int(item))
            except:
                continue

        plt.plot(finalXs, finalYs)


        file = "/home/amirhossein/Documents/GitHub/new-temp/input files/pollutionData158355.csv"
        fh = open(file)
        csvReader = csv.reader(fh)

        # generates headers and rows lists
        headers = next(csvReader)

        df = pd.read_csv(file, names=headers)

        # df['timestamp'] = df['timestamp'].map(lambda x: datetime.strptime(str(x), "%Y-%m-%d %H:%M:%S"))
        x = df['timestamp']
        y = df["carbon_monoxide"]
        finalYs = []
        finalXs = []
        for i in range(1, len(x)):
            finalXs.append(x[i])
        for item in y:
            try:
                finalYs.append(int(item))
            except:
                continue


        plt.plot(finalXs, finalYs)
        plt.gcf().autofmt_xdate()

        plt.xlabel('Load On Sample')
        plt.ylabel('Displacement Into Surface')
        plt.gca().set_xticks([0, 500, 1000, 1500, 2000])
        plt.gca().set_yticks([0, 50, 100, 150, 200])
        plt.show()


