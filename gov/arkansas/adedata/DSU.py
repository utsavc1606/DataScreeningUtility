'''
Created on Feb 10, 2016

@author: utsavchatterjee
'''
import csv
import time
from nltk.probability import FreqDist
from collections import OrderedDict
import re
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os

gmail_user = "ade.dsu@gmail.com"
gmail_pwd = "adeere123$"


ControlFile = open("DSU_Control.txt", "r")
ControlDict = {}
for line in ControlFile:
    (key, val) = line.split("=")
    ControlDict[key.strip()] = val.strip()

ReportFile = open(ControlDict['OutputReportPath'], 'w')
start_time = time.time()
 
def BasicCounts(FileName):
    ReportFile.write("\n\n#### BASIC FACTS ####")
    LineCount = 0
    f = open(FileName, 'r')
    reader = csv.reader(f, delimiter ='|')
    Headers = next(reader)
    for rows in reader:
        LineCount += 1
        
    ReportFile.write("\nFile Name = "+ FileName)    
    ReportFile.write("\nNumber of rows = " + str(LineCount))
    ReportFile.write("\nNumber of columns = " + str(len(Headers)) + "\n")
#     print "Basic Facts: Complete"

#     ReportFile.write("Process time = " + str(time.time() - start_time) + " seconds \n"
     
def CheckRowOffset(FileName):
    ReportFile.write("\n#### CHECKING ROW OFFSETS ####")
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
    ReportFile.write("\nErrors found = " + str(ErrorCount))
#     ReportFile.write("Process time = " + str(time.time() - start_time) + " seconds")
#     print "Check Row Offsets: Complete"
 
def CheckSSNStats(FileName):
    SSNCount = 0
#     ReportFile.write(" \n#### CALCULATING SSN STATISTICS ####"
    f = open(FileName, 'r')
    reader = csv.reader(f, delimiter ='|')
#     Headers = next(reader)
    for rows in reader:
        if rows[3].strip() != "":
            SSNCount += 1
    return SSNCount
#     ReportFile.write("Process time = " + str(time.time() - start_time) + " seconds"
     
def SSNFrequency(FileName):
    SSNList = []
    f = open(FileName, 'r')
    reader = csv.reader(f, delimiter ='|')
#     Headers = next(reader)
    for rows in reader:
        SSNList.append(rows[3].strip())
    return SSNList    
 
def SortSSNFrequency(FileName):
    ReportFile.write("\n\n#### SSN STATISTICS ####")
    ReportFile.write("\nTotal SSN count = "+str(CheckSSNStats(FileName)))
#     x = np.array(SSNFrequency(FileName))
    fdist = FreqDist(SSNFrequency(FileName))
    frequencies = OrderedDict(sorted(fdist.items(), key = lambda x:x[1], reverse = True))
    ReportFile.write("\nDistinct SSN count = " + str(len(frequencies)))
    ReportFile.write("\n\n#### TOP 10 FREQUENCIES ####")
    for k, v in frequencies.items()[:10]:
        ReportFile.write("\n"+k+"    "+ str(v))
     
def CheckFNStats(FileName):
    FNCount = 0
#     ReportFile.write(" \n#### CALCULATING SSN STATISTICS ####"
    f = open(FileName, 'r')
    reader = csv.reader(f, delimiter ='|')
#     Headers = next(reader)
    for rows in reader:
        if rows[0].strip() != "":
            FNCount += 1
    return FNCount
     
def FNFrequency(FileName):
    FNList = []
    f = open(FileName, 'r')
    reader = csv.reader(f, delimiter ='|')
#     Headers = next(reader)
    for rows in reader:
        FNList.append(rows[0].strip())
    return FNList    
 
def SortFNFrequency(FileName):
    ReportFile.write("\n\n#### FN STATISTICS ####")
    ReportFile.write("\nTotal FN count = "+str(CheckFNStats(FileName)))
#     x = np.array(FNFrequency(FileName))
    fdist = FreqDist(FNFrequency(FileName))
    frequencies = OrderedDict(sorted(fdist.items(), key = lambda x:x[1], reverse = True))
    ReportFile.write("\nDistinct FN count = " + str(len(frequencies)))
    ReportFile.write("\n\n#### TOP 10 FREQUENCIES ####")
    for k, v in frequencies.items()[:10]:
        ReportFile.write("\n"+k+"    "+str(v))
 
def CheckLNStats(FileName):
    LNCount = 0
    f = open(FileName, 'r')
    reader = csv.reader(f, delimiter ='|')
#     Headers = next(reader)
    for rows in reader:
        if rows[2].strip() != "":
            LNCount += 1
    return LNCount
     
def LNFrequency(FileName):
    LNList = []
    f = open(FileName, 'r')
    reader = csv.reader(f, delimiter ='|')
#     Headers = next(reader)
    for rows in reader:
        LNList.append(rows[2].strip())
    return LNList    
 
def SortLNFrequency(FileName):
    ReportFile.write("\n\n#### LN STATISTICS ####")
    ReportFile.write("\nTotal LN count = "+str(CheckFNStats(FileName)))
#     x = np.array(LNFrequency(FileName))
    fdist = FreqDist(LNFrequency(FileName))
    frequencies = OrderedDict(sorted(fdist.items(), key = lambda x:x[1], reverse = True))
    ReportFile.write("\nDistinct LN count = " + str(len(frequencies)))
    ReportFile.write("\n\n#### TOP 10 FREQUENCIES ####")
    for k, v in frequencies.items()[:10]:
        ReportFile.write("\n"+k+"    "+str(v))
     
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
#     Headers = next(reader)
    for rows in reader:
        DOBList.append(rows[4].strip())
    return DOBList    
 
def SortDOBFrequency(FileName):
    ReportFile.write("\n\n#### DOB STATISTICS ####")
    ReportFile.write("\nTotal DOB count = "+str(CheckFNStats(FileName)))
#     x = np.array(DOBFrequency(FileName))
    fdist = FreqDist(DOBFrequency(FileName))
    frequencies = OrderedDict(sorted(fdist.items(), key = lambda x:x[1], reverse = True))
    ReportFile.write("\nDistinct DOB count = " + str(len(frequencies)))
    ReportFile.write("\n\n#### TOP 10 FREQUENCIES ####")
    for k, v in frequencies.items()[:10]:
        ReportFile.write("\n"+k+"    "+str(v))
         
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
    ReportFile.write("\n\n#### ResearchID STATISTICS ####")
    ReportFile.write("\nTotal RID count = "+str(CheckRIDStats(FileName)))
#     x = np.array(RIDFrequency(FileName))
    fdist = FreqDist(RIDFrequency(FileName))
    frequencies = OrderedDict(sorted(fdist.items(), key = lambda x:x[1], reverse = True))
    ReportFile.write("\nDistinct ResearchID count = " + str(len(frequencies)))
    ReportFile.write("\n\n#### TOP 10 FREQUENCIES ####")
    for k, v in frequencies.items()[:10]:
        ReportFile.write("\n"+k+"    "+str(v))
    ReportFile.write("\n\n#### BOTTOM 10 FREQUENCIES ####")
    for k, v in frequencies.items()[len(frequencies)-10:]:
        ReportFile.write("\n"+k+"    "+str(v))
     
def CleanseData(FileName):
    ReportFile.write("\n\n#### CLEANSING DATA ####")
    d = open(FileName, "r")
    op = open(ControlDict['CleansedFilePath'], "w")
    for row in d:
        op.write(re.sub('[^A-Za-z0-9|\s\n.]+', '', row))
    d.close()    
    ReportFile.write("\nComplete: Cleansed file located at - " + ControlDict['CleansedFilePath'])
#     ReportFile.write("\nProcess time = " + str(time.time() - start_time) + " seconds")
     
def CheckHeaders(FileName):
    ReportFile.write("#### CHECKING HEADERS ####")
    f = open(FileName, 'r')
    reader = csv.reader(f, delimiter ='|')
    Headers = next(reader)
    HeaderList = ["FirstName", "MiddleName", "LastName", "SSN", "DOB"]
    for h in Headers[:5]:
        if h not in HeaderList:
            ReportFile.write("\nError in Headers. Please review.")
        else:
            ReportFile.write("\nNo Errors.")
             
def ReviewProcessedOutput(FileName):
    SortRIDFrequency(FileName)
    
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
    
if 'ProcessedFilePath' in ControlDict.keys(): 
    CheckHeaders(ControlDict['SourceFilePath'])
    print "Check Headers: Complete"             
    BasicCounts(ControlDict['SourceFilePath'])        
    print "Check Basic Counts: Complete"
    CheckRowOffset(ControlDict['SourceFilePath'])
    print "Check Row Offset: Complete"
    CheckSSNStats(ControlDict['SourceFilePath'])
    SortSSNFrequency(ControlDict['SourceFilePath'])
    print "Check SSN Statistics: Complete"
    CheckFNStats(ControlDict['SourceFilePath'])
    SortFNFrequency(ControlDict['SourceFilePath'])    
    print "Check FN Statistics: Complete"
    CheckLNStats(ControlDict['SourceFilePath'])
    SortLNFrequency(ControlDict['SourceFilePath']) 
    print "Check LN Statistics: Complete"
    CheckDOBStats(ControlDict['SourceFilePath'])
    SortDOBFrequency(ControlDict['SourceFilePath'])      
    print "Check DOB Statistics: Complete"
    CleanseData(ControlDict['SourceFilePath'])
    print "Cleanse Data: Complete"
    ReviewProcessedOutput(ControlDict['ProcessedFilePath'])
    print "Review Processed Output: Complete" 
    ReportFile.write("\nProcess time = " + str(time.time() - start_time) + " seconds")
#     print "Process time = " + str(time.time() - start_time) + " seconds"
else:
    CheckHeaders(ControlDict['SourceFilePath'])
    print "Check Headers: Complete"             
    BasicCounts(ControlDict['SourceFilePath'])        
    print "Check Basic Counts: Complete"
    CheckRowOffset(ControlDict['SourceFilePath'])
    print "Check Row Offset: Complete"
    CheckSSNStats(ControlDict['SourceFilePath'])
    SortSSNFrequency(ControlDict['SourceFilePath'])
    print "Check SSN Statistics: Complete"
    CheckFNStats(ControlDict['SourceFilePath'])
    SortFNFrequency(ControlDict['SourceFilePath'])    
    print "Check FN Statistics: Complete"
    CheckLNStats(ControlDict['SourceFilePath'])
    SortLNFrequency(ControlDict['SourceFilePath']) 
    print "Check LN Statistics: Complete"
    CheckDOBStats(ControlDict['SourceFilePath'])
    SortDOBFrequency(ControlDict['SourceFilePath'])      
    print "Check DOB Statistics: Complete"
    CleanseData(ControlDict['SourceFilePath'])
    print "Cleanse Data: Complete"
    ReportFile.write("Process time = " + str(time.time() - start_time) + " seconds")
#     print "Process time = " + str(time.time() - start_time) + " seconds"

ControlFile.close()
ReportFile.close()
mail("utsav.chatterjee@arkansas.gov",
   "Data Screen Utility: File Analysis Report",
   "Data Screen Utility: File Analysis Report for "+ ControlDict['SourceFilePath'],
   ControlDict['OutputReportPath'])
print "Email Transmission: Complete"
print "Process time = " + str(time.time() - start_time) + " seconds"

