'''
Created on Feb 18, 2016
@author: utsavchatterjee
'''
import csv
from nltk.probability import FreqDist
from collections import OrderedDict
import re
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os
import time

try:
    ControlFile = open("DSU_Control.txt", "r")
    ControlDict = {}
    for line in ControlFile:
        try:
            (key, val) = line.split("=")
            ControlDict[key.strip()] = val.strip()
        except:
            print "Dictionary Error with DSU_Control.txt"   
except IOError:
    print "DSU_Control.txt not found."            
gmail_user = ControlDict['sender_id']
gmail_pwd = ControlDict['sender_password']
    
ReportFile = open(ControlDict['OutputReportPath'], 'w')
start_time = time.time()


BasicCountsDict = {} 
SSNStatsDict = {}
SSNFDDict = {}
RIDFDDict = {}
RIDStatsDict = {}
FNStatsDict = {}
FNFDDict = {}
LNStatsDict = {}
LNFDDict = {}
DOBStatsDict = {}
DOBFDDict = {}


def BasicCounts(FileName):
    LineCount = 0
    f = open(FileName, 'r')
    reader = csv.reader(f, delimiter ='|')
    Headers = next(reader)
    for line in reader:
        LineCount += 1
    BasicCountsDict['FileName'] = FileName    
    BasicCountsDict['NumRows'] = str(LineCount)
    BasicCountsDict['NumColumns'] = str(len(Headers))
    print "Basic counts: Complete"

def CheckRowOffset(FileName):
    ErrorOutputFile = open(ControlDict['OffsetRows'], 'w')
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
    if ErrorCount > 0:
        ReportFile.write("\nOffset Test: Failed. Please check offset rows at location "+ ControlDict['OffsetRows'])
    else:
        ReportFile.write("\nOffset Test: Passed.")
    print "Row Offset Check: Complete"
    
def CheckHeaders(FileName):
    f = open(FileName, 'r')
    reader = csv.reader(f, delimiter ='|')
    Headers = next(reader)
    if (Headers[0]=="FirstName" and Headers[1]=="MiddleName" and Headers[2]=="LastName" and Headers[3]=="SSN" and Headers[4]=="DOB"):
        ReportFile.write ("\nHeaders Test: Passed")
    else:
        ReportFile.write ("\nHeaders Test: Failed. Please check first 5 headers.")
    print "Check Headers: Complete"
    
def CheckSSNStats(FileName):
    SSNList = []
    f = open(FileName, 'r')
    reader = csv.reader(f, delimiter ='|')
    for line in reader:
        SSNList.append(line[3].strip())
    SSNStatsDict['SSNCount'] = len(SSNList)-1
    fdist = FreqDist(SSNList)
    frequencies = OrderedDict(sorted(fdist.items(), key = lambda x:x[1], reverse = True))
    SSNStatsDict['DistinctSSNCount'] = len(frequencies)
    for k, v in frequencies.items()[:10]:
        SSNFDDict[k]=v
    SSNStatsDict['FreqDist'] = SSNFDDict
    print "Check SSN Stats: Complete"
    
def CheckRIDStats(FileName):
    RIDList = []
    f = open(FileName, 'r')
    reader = csv.reader(f, delimiter ='|')
    for line in reader:
        RIDList.append(line[0].strip())
    RIDStatsDict['RIDCount'] = len(RIDList)-1
    fdist = FreqDist(RIDList)
    frequencies = OrderedDict(sorted(fdist.items(), key = lambda x:x[1], reverse = True))
    RIDStatsDict['DistinctRIDCount'] = len(frequencies)
    for k, v in frequencies.items()[:10]:
        RIDFDDict[k]=v
    RIDStatsDict['FreqDist'] = RIDFDDict    
    print "Check RID Stats: Complete"
    
def CheckFNStats(FileName):
    FNList = []
    f = open(FileName, 'r')
    reader = csv.reader(f, delimiter ='|')
    for line in reader:
        FNList.append(line[0].strip())
    FNStatsDict['FNCount'] = len(FNList)-1
    fdist = FreqDist(FNList)
    frequencies = OrderedDict(sorted(fdist.items(), key = lambda x:x[1], reverse = True))
    FNStatsDict['DistinctFNCount'] = len(frequencies)
    for k, v in frequencies.items()[:10]:
        FNFDDict[k]=v
    FNStatsDict['FreqDist'] = FNFDDict    
    print "Check FN Stats: Complete"

def CheckLNStats(FileName):
    LNList = []
    f = open(FileName, 'r')
    reader = csv.reader(f, delimiter ='|')
    for line in reader:
        LNList.append(line[2].strip())
    LNStatsDict['LNCount'] = len(LNList) - 1
    fdist = FreqDist(LNList)
    frequencies = OrderedDict(sorted(fdist.items(), key = lambda x:x[1], reverse = True))
    LNStatsDict['DistinctLNCount'] = len(frequencies)
    for k, v in frequencies.items()[:10]:
        LNFDDict[k]=v
    LNStatsDict['FreqDist'] = LNFDDict
    print "Check LN Stats: Complete"

def CheckDOBStats(FileName):
    DOBList = []
    f = open(FileName, 'r')
    reader = csv.reader(f, delimiter ='|')
    for line in reader:
        DOBList.append(line[4].strip())
    DOBStatsDict['DOBCount'] = len(DOBList)-1
    fdist = FreqDist(DOBList)
    frequencies = OrderedDict(sorted(fdist.items(), key = lambda x:x[1], reverse = True))
    DOBStatsDict['DistinctDOBCount'] = len(frequencies)
    for k, v in frequencies.items()[:10]:
        DOBFDDict[k]=v
    DOBStatsDict['FreqDist'] = DOBFDDict
    print "Check DOB Stats: Complete"

def CleanseData(FileName):
    d = open(FileName, 'r')
    op = open(ControlDict['CleansedFilePath'], "w")
    for row in d:
        op.write(re.sub('[^A-Za-z0-9|\s\n.]+', '', row))
    d.close()
    print "Cleanse Data: Complete"

def mail(to, subject, text, attach):
    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(text))
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(open(attach, 'rb').read())
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition','attachment; filename="%s"' % os.path.basename(attach))
    msg.attach(part)
    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmail_user, gmail_pwd)
    mailServer.sendmail(gmail_user, to, msg.as_string())
    # Should be mailServer.quit(), but that crashes...
    mailServer.close()
    print "Email transmission: Complete"

if 'SourceFilePath' in ControlDict.keys() and 'ProcessedFilePath' in ControlDict.keys():
    BasicCounts(ControlDict['SourceFilePath'])
    ReportFile.write("Basic Information: Source File")
    ReportFile.write("\nFile Name = " + BasicCountsDict['FileName'])
    ReportFile.write("\nTotal row count = " + BasicCountsDict['NumRows'])
    ReportFile.write("\nTotal column count = " + BasicCountsDict['NumColumns'])
    ReportFile.write("\n______________________________________________________")
    
    BasicCounts(ControlDict['ProcessedFilePath'])
    ReportFile.write("\nBasic Information: Processed File")
    ReportFile.write("\nFile Name = " + BasicCountsDict['FileName'])
    ReportFile.write("\nTotal row count = " + BasicCountsDict['NumRows'])
    ReportFile.write("\nTotal column count = " + BasicCountsDict['NumColumns'])
    ReportFile.write("\n______________________________________________________")
    
    CheckHeaders(ControlDict['SourceFilePath'])
    ReportFile.write("\n______________________________________________________")

    CheckRowOffset(ControlDict['SourceFilePath'])
    ReportFile.write("\n______________________________________________________")
    
    CheckSSNStats(ControlDict['SourceFilePath'])
    ReportFile.write("\nSSN Statistics")
    ReportFile.write("\nTotal SSN count (Source File)= "+ str(SSNStatsDict['SSNCount']))
    ReportFile.write("\nDistinct SSN count = "+ str(SSNStatsDict['DistinctSSNCount']))
    ReportFile.write("\nTop 10 frequencies = " + str(SSNStatsDict['FreqDist']))
    ReportFile.write("\n______________________________________________________") 
    
    CheckRIDStats(ControlDict['ProcessedFilePath'])
    ReportFile.write("\nResearchID Statistics")
    ReportFile.write("\nTotal RID count (Processed File)= "+ str(RIDStatsDict['RIDCount']))
    ReportFile.write("\nDistinct RID count = "+ str(RIDStatsDict['DistinctRIDCount']))
    ReportFile.write("\nTop 10 frequencies = " + str(RIDStatsDict['FreqDist']))
    ReportFile.write("\n______________________________________________________")
    
    CheckFNStats(ControlDict['SourceFilePath'])
    ReportFile.write("\nFirst Name Statistics")
    ReportFile.write("\nTotal FN count (Source File)= "+ str(FNStatsDict['FNCount']))
    ReportFile.write("\nDistinct FN count = "+ str(FNStatsDict['DistinctFNCount']))
    ReportFile.write("\nTop 10 frequencies = " + str(FNStatsDict['FreqDist']))
    ReportFile.write("\n______________________________________________________")
    
    CheckLNStats(ControlDict['SourceFilePath'])
    ReportFile.write("\nLast Name Statistics")
    ReportFile.write("\nTotal LN count (Source File)= "+ str(LNStatsDict['LNCount']))
    ReportFile.write("\nDistinct LN count = "+ str(LNStatsDict['DistinctLNCount']))
    ReportFile.write("\nTop 10 frequencies = " + str(LNStatsDict['FreqDist']))
    ReportFile.write("\n______________________________________________________")
    
    CheckDOBStats(ControlDict['SourceFilePath'])
    ReportFile.write("\nDate of Birth Statistics")
    ReportFile.write("\nTotal DOB count (Source File)= "+ str(DOBStatsDict['DOBCount']))
    ReportFile.write("\nDistinct DOB count = "+ str(DOBStatsDict['DistinctDOBCount']))
    ReportFile.write("\nTop 10 frequencies = " + str(DOBStatsDict['FreqDist']))
    ReportFile.write("\n______________________________________________________")
    
    
    if str(ControlDict['CleanseData?']).upper() == "YES":
        CleanseData(ControlDict['SourceFilePath'])
    
elif 'SourceFilePath' in ControlDict.keys() and 'ProcessedFilePath' not in ControlDict.keys():
    BasicCounts(ControlDict['SourceFilePath'])
    ReportFile.write("\nBasic Information: Source File")
    ReportFile.write("\nFile Name = " + BasicCountsDict['FileName'])
    ReportFile.write("\nTotal row count = " + BasicCountsDict['NumRows'])
    ReportFile.write("\nTotal column count = " + BasicCountsDict['NumColumns'])
    ReportFile.write("\n______________________________________________________")

    CheckRowOffset(ControlDict['SourceFilePath'])
    ReportFile.write ("\n______________________________________________________")
    
    CheckSSNStats(ControlDict['SourceFilePath'])
    ReportFile.write("\nSSN Statistics")
    ReportFile.write ("\nTotal SSN count (Source File) = "+ str(SSNStatsDict['SSNCount']))
    ReportFile.write ("\nDistinct SSN count = "+ str(SSNStatsDict['DistinctSSNCount']))
    ReportFile.write ("\nTop 10 frequencies = " + str(SSNStatsDict['FreqDist']))
    ReportFile.write ("\n______________________________________________________") 
        
    CheckFNStats(ControlDict['SourceFilePath'])
    ReportFile.write("\nFirst Name Statistics")
    ReportFile.write("\nTotal FN count (Source File)= "+ str(FNStatsDict['FNCount']))
    ReportFile.write("\nDistinct FN count = "+ str(FNStatsDict['DistinctFNCount']))
    ReportFile.write("\nTop 10 frequencies = " + str(FNStatsDict['FreqDist']))
    ReportFile.write("\n______________________________________________________")
    
    CheckLNStats(ControlDict['SourceFilePath'])
    ReportFile.write("\nLast Name Statistics")
    ReportFile.write("\nTotal LN count (Source File)= "+ str(LNStatsDict['LNCount']))
    ReportFile.write("\nDistinct LN count = "+ str(LNStatsDict['DistinctLNCount']))
    ReportFile.write("\nTop 10 frequencies = " + str(LNStatsDict['FreqDist']))
    ReportFile.write("\n______________________________________________________")
    
    CheckDOBStats(ControlDict['SourceFilePath'])
    ReportFile.write("\nDate of Birth Statistics")
    ReportFile.write("\nTotal DOB count (Source File)= "+ str(DOBStatsDict['DOBCount']))
    ReportFile.write("\nDistinct DOB count = "+ str(DOBStatsDict['DistinctDOBCount']))
    ReportFile.write("\nTop 10 frequencies = " + str(DOBStatsDict['FreqDist']))
    ReportFile.write("\n______________________________________________________")
    
    
    if str(ControlDict['CleanseData?']).upper() == "YES":
        CleanseData(ControlDict['SourceFilePath'])
    
elif 'SourceFilePath' not in ControlDict.keys() and 'ProcessedFilePath' in ControlDict.keys():
    BasicCounts(ControlDict['ProcessedFilePath'])
    ReportFile.write("\nBasic Information: Processed File")
    ReportFile.write("\nFile Name = " + BasicCountsDict['FileName'])
    ReportFile.write("\nTotal row count = " + BasicCountsDict['NumRows'])
    ReportFile.write("\nTotal column count = " + BasicCountsDict['NumColumns'])
    ReportFile.write("\n______________________________________________________")
    
    CheckRIDStats(ControlDict['ProcessedFilePath'])
    ReportFile.write("\nResearchID Statistics")
    ReportFile.write("\nTotal RID count (Processed File)= "+ str(RIDStatsDict['RIDCount']))
    ReportFile.write("\nDistinct RID count = "+ str(RIDStatsDict['DistinctRIDCount']))
    ReportFile.write("\nTop 10 frequencies = " + str(RIDStatsDict['FreqDist']))
    ReportFile.write("\n______________________________________________________")
    

ReportFile.write("\nProcess time = " + str(time.time() - start_time) + " seconds")        
ReportFile.write("\n______________________________________________________")
ReportFile.write("\nEmail Transmission: Complete")
ReportFile.close()
mail(ControlDict['email_recipient'],
   "Data Screen Utility: File Analysis Report",
   "Data Screen Utility: File Analysis Report for "+ ControlDict['SourceFilePath'],
   ControlDict['OutputReportPath'])
ControlFile.close()
raw_input("Process Complete. Press Enter to Exit.")
