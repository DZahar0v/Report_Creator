import json
import os
import sys

class Finding:
    def __init__(self, _status, _name, _description, _recommendationText, _lang):
        self.status = _status
        self.name = _name
        self.description = _description
        self.recommendationText = _recommendationText
        self.recommendationCode = ""
        self.lines = []
        if (_lang.upper() == "SOL"):
            self.lang = "solidity"
        elif (_lang.upper() == "VY"):
            self.lang = "vyper"
        else:
            self.lang = ""

    def addLine(self, _line, _file):
        self.lines.append((_file, _line))
        return

    def addCode(self, _code):
        self.recommendationCode = _code
        return

Findings = {}
FindingString = "// FINDING:"
StatusString = "STATUS |"
NameString = "NAME |"
DescriptionString = "DESC |"
RecommendationTextString = "REC_TEXT |"
RecommendationCodeString = "REC_CODE |"

def scanFile(fileName):
    code = open(fileName, "r")        
    lineCount = 1
    bFind = False
    line = ""
    _, file_extension = os.path.splitext(fileName)

    while True:
        if not(bFind):
            line = code.readline()            
        else:
            bFind = False
        if not(line): 
            break

        if (FindingString in line):
            # read status and name
            try:
                stIndex = line.index(StatusString)
            except Exception:
                print("STATE |...| not found in " + fileName + " on line " + str(lineCount))
                continue
            try:
                nmIndex = line.index(NameString)
            except Exception:
                print("NAME |...| not found in " + fileName + " on line " + str(lineCount))
                continue
            status = line[stIndex+8 : nmIndex-2]
            name = line[nmIndex+6 : len(line)-2]
            key = status + '_' + name                
            print("Finding status: " + status + " name: " + name)
            if key in Findings:
                Findings[key].addLine(lineCount, fileName)                
            else:    
                # read description
                line = code.readline()            
                try:
                    dsIndex = line.index(DescriptionString)                        
                except Exception:
                    print("DESC |...| not found in " + fileName + " on line " + str(lineCount))
                    continue
                desc = line[dsIndex+6 : len(line)-2]
                # read recommendation text
                line = code.readline()            
                try:
                    rtIndex = line.index(RecommendationTextString)                        
                except Exception:
                    print("REC_TEXT |...| not found in " + fileName + " on line " + str(lineCount))
                    continue    
                recText = line[rtIndex+10 : len(line)-2]
                # read recommendation code if exist
                line = code.readline()            
                recCode = ""
                while (RecommendationCodeString in line):
                    rcIndex = line.index(RecommendationCodeString)                        
                    if (recCode != ""):
                        recCode = recCode + '\n'
                    recCode = recCode + line[rcIndex+10 : len(line)-2]
                    line = code.readline()                
                bFind = True
                # add finding to map                                
                Findings[key] = Finding(status, name, desc, recText, file_extension[1:])
                Findings[key].addLine(lineCount, fileName)
                if (recCode != ""):
                    Findings[key].addCode(recCode)
        else:
            lineCount = lineCount + 1

    code.close()
    return

def FillReportByKeys(keys, file, status, path):
    file.write("### " + status + "\n")    
    if (len(keys) == 0):        
        file.write("Not found\n\n")        
    else:
        findingCount = 1
        for key in keys:
            name = Findings[key].name
            desc = Findings[key].description
            recText = Findings[key].recommendationText
            lines = Findings[key].lines
            recCode = Findings[key].recommendationCode
            ext = Findings[key].lang            
            file.write("#### " + str(findingCount) + ". " + name + "\n")
            file.write("##### Description\n")
            file.write(desc + "\n")
            for line in lines:
                file.write(path + "/" + line[0] + "#L" + str(line[1]) + "\n")
            file.write("##### Recommendation\n")
            file.write(recText + "\n")
            if (recCode != ""):
                file.write("```" + ext + "=\n")
                file.write(recCode + "\n")
                file.write("```\n")
            file.write("##### Status\n")
            file.write("NEW\n")
            file.write("##### Client's commentary\n")        
            file.write("> comment here\n\n")
            findingCount += 1    
    return

def CreateReport(fileName, path, files):
    Critical_keys = []
    Major_keys = []
    Warning_keys = []
    Comment_keys = []
    # Collect all keys
    for key in Findings.keys():
        if (Findings[key].status == "CRITICAL"): Critical_keys.append(key)
        elif (Findings[key].status == "MAJOR"): Major_keys.append(key)
        elif (Findings[key].status == "WARNING"): Warning_keys.append(key)
        elif (Findings[key].status == "COMMENT"): Comment_keys.append(key)
    # Create report
    report = open(fileName, "w")    
    report.write("### Scope of the Audit\n")
    report.write("The scope of the audit includes the following smart contracts at:\n")
    for file in files:
        report.write(path + "/" + file + "\n")
    report.write("\n")
    FillReportByKeys(Critical_keys, report, "CRITICAL", path)
    FillReportByKeys(Major_keys, report, "MAJOR", path)
    FillReportByKeys(Warning_keys, report, "WARNINGS", path)
    FillReportByKeys(Comment_keys, report, "COMMENTS", path)
    report.close()
    return

if __name__ == "__main__":    
    outFile = str(sys.argv[1])
    basePath = str(sys.argv[2])    
    #outFile = "Report.md"
    #basePath = https://github.com/xorder-finance/xorder-contracts/blob/main

    with open("ReportConfig.json") as jsonFile:
        jsonObject = json.load(jsonFile)
        jsonFile.close()
    filesList = jsonObject['files']

    for root, dirs, files in os.walk("."):
        path = root.split(os.sep)
        file_prefix = ""
        for i in range(1,len(path)):
            file_prefix = file_prefix + path[i] + "/"
        for file in files:            
            fileName = file_prefix + file
            if (fileName in filesList):
                print("Working with " + fileName + "...")
                scanFile(fileName)

    CreateReport(outFile, basePath, filesList)