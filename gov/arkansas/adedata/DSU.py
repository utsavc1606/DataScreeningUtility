'''
Created on Feb 10, 2016

@author: utsavchatterjee
'''
import csv
import time
import numpy as np
from StdSuites.Table_Suite import rows
from nltk.probability import FreqDist
from collections import OrderedDict
import sys
import re

sys.stdout = open("Analysis.txt", 'w')
start_time = time.time()

def BasicCounts(FileName):
    print "\n#### BASIC FACTS ####"
    LineCount = 0
    f = open(FileName, 'r')
    reader = csv.reader(f, delimiter ='|')
    Headers = next(reader)
    for rows in reader:
        LineCount += 1
    print "File Name = "+ FileName    
    print "Number of rows = " + str(LineCount)
    print "Number of columns = " + str(len(Headers)) + "\n"
#     print "Process time = " + str(time.time() - start_time) + " seconds \n"
    
def CheckRowOffset(FileName):
    print "#### CHECKING ROW OFFSETS ####"
    ErrorOutputFile = open("OffsetRows.txt", 'w')
    LineCount = 1
    ErrorCount = 0
    f = open(FileName, 'r')
    reader = csv.reader(f, delimiter ='|')
    Headers = next(reader)
    for rows in reader:
        if len(rows) != len(Headers):
            ErrorCount += 1
            ErrorOutputFile.write("Row Location = "+ str(LineCount) + "\n") 
            ErrorOutputFile.write("Row data = "+ "|".join(rows) + "\n")
        LineCount += 1
    print "Errors found = " + str(ErrorCount)
#     print "Process time = " + str(time.time() - start_time) + " seconds"

def CheckSSNStats(FileName):
    SSNCount = 0
#     print " \n#### CALCULATING SSN STATISTICS ####"
    f = open(FileName, 'r')
    reader = csv.reader(f, delimiter ='|')
    Headers = next(reader)
    for rows in reader:
        if rows[3].strip() != "":
            SSNCount += 1
    return SSNCount
#     print "Process time = " + str(time.time() - start_time) + " seconds"
    
def SSNFrequency(FileName):
    SSNList = []
    f = open(FileName, 'r')
    reader = csv.reader(f, delimiter ='|')
    Headers = next(reader)
    for rows in reader:
        SSNList.append(rows[3].strip())
    return SSNList    

def SortSSNFrequency(FileName):
    print " \n#### SSN STATISTICS ####"
    print "Total SSN count = "+str(CheckSSNStats(FileName))
    x = np.array(SSNFrequency(FileName))
    fdist = FreqDist(SSNFrequency(FileName))
    frequencies = OrderedDict(sorted(fdist.items(), key = lambda x:x[1], reverse = True))
    print "Distinct SSN count = " + str(len(frequencies))
    print "\nXXXX TOP 10 FREQUENCIES XXXX"
    for k, v in frequencies.items()[:10]:
        print k, v
    
def CheckFNStats(FileName):
    FNCount = 0
#     print " \n#### CALCULATING SSN STATISTICS ####"
    f = open(FileName, 'r')
    reader = csv.reader(f, delimiter ='|')
    Headers = next(reader)
    for rows in reader:
        if rows[0].strip() != "":
            FNCount += 1
    return FNCount
    
def FNFrequency(FileName):
    FNList = []
    f = open(FileName, 'r')
    reader = csv.reader(f, delimiter ='|')
    Headers = next(reader)
    for rows in reader:
        FNList.append(rows[0].strip())
    return FNList    

def SortFNFrequency(FileName):
    print " \n#### FN STATISTICS ####"
    print "Total FN count = "+str(CheckFNStats(FileName))
    x = np.array(FNFrequency(FileName))
    fdist = FreqDist(FNFrequency(FileName))
    frequencies = OrderedDict(sorted(fdist.items(), key = lambda x:x[1], reverse = True))
    print "Distinct FN count = " + str(len(frequencies))
    print "\nXXXX TOP 10 FREQUENCIES XXXX"
    for k, v in frequencies.items()[:10]:
        print k, v

def CheckLNStats(FileName):
    LNCount = 0
    f = open(FileName, 'r')
    reader = csv.reader(f, delimiter ='|')
    Headers = next(reader)
    for rows in reader:
        if rows[2].strip() != "":
            LNCount += 1
    return LNCount
    
def LNFrequency(FileName):
    LNList = []
    f = open(FileName, 'r')
    reader = csv.reader(f, delimiter ='|')
    Headers = next(reader)
    for rows in reader:
        LNList.append(rows[2].strip())
    return LNList    

def SortLNFrequency(FileName):
    print " \n#### LN STATISTICS ####"
    print "Total LN count = "+str(CheckFNStats(FileName))
    x = np.array(LNFrequency(FileName))
    fdist = FreqDist(LNFrequency(FileName))
    frequencies = OrderedDict(sorted(fdist.items(), key = lambda x:x[1], reverse = True))
    print "Distinct LN count = " + str(len(frequencies))
    print "\nXXXX TOP 10 FREQUENCIES XXXX"
    for k, v in frequencies.items()[:10]:
        print k, v
    
def CheckDOBStats(FileName):
    DOBCount = 1
    f = open(FileName, 'r')
    reader = csv.reader(f, delimiter ='|')
    for rows in reader:
        if rows[4].strip() != "":
            DOBCount += 1
    return DOBCount
    
def DOBFrequency(FileName):
    DOBList = []
    f = open(FileName, 'r')
    reader = csv.reader(f, delimiter ='|')
    Headers = next(reader)
    for rows in reader:
        DOBList.append(rows[4].strip())
    return DOBList    

def SortDOBFrequency(FileName):
    print " \n#### DOB STATISTICS ####"
    print "Total DOB count = "+str(CheckFNStats(FileName))
    x = np.array(DOBFrequency(FileName))
    fdist = FreqDist(DOBFrequency(FileName))
    frequencies = OrderedDict(sorted(fdist.items(), key = lambda x:x[1], reverse = True))
    print "Distinct DOB count = " + str(len(frequencies))
    print "\nXXXX TOP 10 FREQUENCIES XXXX"
    for k, v in frequencies.items()[:10]:
        print k, v
        
def CheckRIDStats(FileName):
    RIDCount = 1
    f = open(FileName, 'r')
    reader = csv.reader(f, delimiter ='|')
    for rows in reader:
        if rows[0].strip() != "":
            RIDCount += 1
    return RIDCount-2
    
def RIDFrequency(FileName):
    RIDList = []
    f = open(FileName, 'r')
    reader = csv.reader(f, delimiter ='|')
#     Headers = next(reader)
    for rows in reader:
        RIDList.append(rows[0].strip())
    return RIDList    

def SortRIDFrequency(FileName):
    print " \n#### ResearchID STATISTICS ####"
    print "Total RID count = "+str(CheckRIDStats(FileName))
    x = np.array(RIDFrequency(FileName))
    fdist = FreqDist(RIDFrequency(FileName))
    frequencies = OrderedDict(sorted(fdist.items(), key = lambda x:x[1], reverse = True))
    print "Distinct ResearchID count = " + str(len(frequencies))
    print "\nXXXX TOP 10 FREQUENCIES XXXX"
    for k, v in frequencies.items()[:10]:
        print k, v

def CleanseData(FileName):
    print " \n#### CLEANSING DATA ####"
    d = open(FileName, "r")
    op = open(FileName[:len(FileName)-4]+"_cleansed", "w")
    for row in d:
        op.write(re.sub('[^A-Za-z0-9|\s\n.]+', '', row))
    d.close()    
    print "\nComplete: Cleansed file located at - <LOCATION>"
    print "\nProcess time = " + str(time.time() - start_time) + " seconds"
    
def CheckHeaders(FileName):
    print "#### CHECKING HEADERS ####"
    f = open(FileName, 'r')
    reader = csv.reader(f, delimiter ='|')
    Headers = next(reader)
    HeaderList = ["FirstName", "MiddleName", "LastName", "SSN", "DOB"]
    for h in Headers[:5]:
        if h not in HeaderList:
            print "Error in Headers. Please review."
        else:
            print "No Errors."
            
def ReviewProcessedOutput(FileName):
    SortRIDFrequency(FileName)

CheckHeaders("TestFile.csv")             
BasicCounts("TestFile.csv")        
CheckRowOffset("TestFile.csv")
CheckSSNStats("TestFile.csv")
SortSSNFrequency("TestFile.csv")
CheckFNStats("TestFile.csv")
SortFNFrequency("TestFile.csv")    
CheckLNStats("TestFile.csv")
SortLNFrequency("TestFile.csv") 
CheckDOBStats("TestFile.csv")
SortDOBFrequency("TestFile.csv")      
CleanseData("TestFile.csv")
ReviewProcessedOutput("TestProcessedFile.csv")

