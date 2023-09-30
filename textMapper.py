"""
import sys

lines = []
try:
    file = open(sys.argv[1], 'r')
    lines = file.readlines()
    file.close()
    print(f"Contents of text file:\n {lines}")
except:
    print("Error opening file.")



input("Waiting to exit...")

"""

import copy
import sys

def retrieveInfo(path):  
   
    fileIn = open(path, 'r', encoding='utf-8')
    lines = fileIn.readlines()
    lines = [x for x in lines if x not in ['\n']]
    lines = [x.strip() for x in lines]
   
    form = lines[0].split()
    current = []
    listHold = []
   
    info = []
   
    formCounter = 0
    lineNum = 1
    while lineNum < len(lines):
       
        todo = form[formCounter % len(form)]
       
        if todo == 's':
            current.append(lines[lineNum])
       
        if todo[0] == 'l':
            while lines[lineNum] != '~':
                listHold.append(lines[lineNum])
                lineNum += 1
            current.append(listHold)
            listHold = []
               
        formCounter += 1
        lineNum += 1
       
        if formCounter % len(form) == 0:
            info.append(current)
            current = []
   
    return info


"""
Get the contents of a file as a list of strings with
the first linem, empty lines, endline characters removed.
"""
def retrieveBasicInfo(path):
   
    try:
        fileIn = open(path, 'r', encoding='utf-8')
        lines = fileIn.readlines()
    except:
        print(f"Error opening file: {path}")
    
    lines = [x for x in lines if x not in ['\n']] # remove empty
    lines = [x.strip() for x in lines] # strip \n
   
    return lines

class Section:
   
    """
   
    """
    def __init__(self, textList=None, parent=None):
       
        self.textList = textList # complete text
        self.elements = [] # lines with commands removed and subsections
        self.parent = parent
        self.selfHold = None # unedited copy of self
        if parent == None: self.makeSelf()
         
    """
    Generate elements from textList. This is done by
    adding non-command string lines to elements, and
    recursively doing the same for subsections.s
    """
    def makeSelf(self, index=0):
        while index < len(self.textList) and "#SECEND" not in self.textList[index]: #self.textList[index] != "#ENDSEC":
            if "#SECSTART" in self.textList[index]: #self.textList[index] == "#STARTSEC":
                newSection = Section(self.textList, self)
                index = newSection.makeSelf(index+1)
                self.elements.append(newSection)
            else:
                self.elements.append(self.textList[index])
            index += 1
        return  index;
   
    """
    Recursively print all strings contained in
    this section and its children.
    """
    def printAll(self):
        for e in self.elements:
            if isinstance(e, str):
                print(e)
            else:
                e.printAll()
        return None
   
    """
    """
    def flattenElements(self, out = []):
        for e in self.elements:
            if isinstance(e, str):
                out.append(e)
            else:
                out = e.flattenElements(out)
        return out
   
    """
    Take info, and
    """
    def mapInfoToSection(self, info, i=0):
        self.selfHold = self.clone()
       
        lineNum = 0
        while lineNum < len(self.elements):
            line = self.elements[lineNum]
            if isinstance(line, str):
                if "{}" in line:
                    self.elements[lineNum] = replaceFirstOccurrance(line, "{}", info[i])
                    i += 1
                    if (i<len(info)) and (info[i] == "~"):
                        return i+1
                else:
                    lineNum += 1
                   
            else:
                i = line.mapInfoToSection(info, i)
                lineNum += 1
               
        if self.parent != None and i < len(info):
            self.parent.elements.insert(self.parent.elements.index(self) + 1, copy.copy(self.selfHold))
            return i
       
    def clone(self):
        clone = Section(self.textList, self.parent)
        clone.elements = copy.deepcopy(self.elements)
        return clone

"""
Replace the first occurance of a substring with another.
"""
def replaceFirstOccurrance(string, old, new, verbose=False):
    if verbose: print(f"Replacing {old} with {new} in {string}")
    index = string.find(old)
    if index != -1:
        return string[:index] + new + string[index + len(old):]
    else:
        return string

def doDefault(path):
   
    formatFilePath = path
    dataFilePath = path[:-9] + ".txt"
    outputFilePath = path[:-9] + ".html"
   
    print("\n")
    print(f"Format file path:  {formatFilePath}")
    print(f"Data file path:    {dataFilePath}")
    print(f"Output file path:  {outputFilePath}")
    print("\n")
   
    inputText = retrieveBasicInfo(formatFilePath)
    sec = Section(inputText, None)
    info = retrieveBasicInfo(dataFilePath)
    sec.mapInfoToSection(info)
       
    with open(outputFilePath, 'w') as file:
        for i in sec.flattenElements():
            file.write(i + "\n")
           
def doWithPrompt():
    formatFilePath = input("Format file path: ")
    dataFilePath = input("Data file path: ")
   
    inputText = retrieveBasicInfo(formatFilePath)
    sec = Section(inputText, None)
    info = retrieveBasicInfo(dataFilePath)
    sec.mapInfoToSection(info)
    sec.printAll()
   
    with open("out.html", 'w') as file:
        for i in sec.flattenElements():
            file.write(i + "\n")


if __name__ == "__main__":
   
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        doDefault(file_path)
    else:
        doWithPrompt()
   
    # lines = []
    # try:
    #     file = open(sys.argv[1], 'r')
    #     lines = file.readlines()
    #     file.close()
    #     print(f"Contents of text file:\n {lines}")
    # except:
    #     print("Error opening file.")



input("Waiting to exit...")

#-------------------------------

# import sys

# def display_file_contents(file_path):
#     try:
#         with open(file_path, 'r') as file:
#             content = file.read()
#             print(content)
#     except FileNotFoundError:
#         print(f"Error: File '{file_path}' not found.")
#     except Exception as e:
#         print(f"An error occurred: {e}")


   
#-------------------------------

# fileIn = open('resumeData/projects.fmt.html', 'r', encoding='utf-8')
# lines = fileIn.readlines()
# lines = [x for x in lines if x not in ['\n']]
# lines = [x.strip() for x in lines]

# lineIndex = 0
# while lineIndex < len(lines):
   
#     line = lines[lineIndex]
#     if "#REPLACE" in line:
       
#         file = line.split()[line.split().index("#REPLACE") + 1]
#         replaceFile = open(file, 'r', encoding='utf-8')
#         replaceLines = replaceFile.readlines()
#         replaceLines = [x for x in replaceLines if x not in ['\n']]
#         replaceLines = [x.strip() for x in replaceLines]
#         lines = lines[:lineIndex] + replaceLines + lines[lineIndex+1:]
       
#     elif "#SECSTART" in line:
       
#         startIndex = lineIndex
#         section = []
#         info = retrieveInfo(line.split()[line.split().index("#SECSTART") + 1])
#         lineIndex += 1
#         line = lines[lineIndex]
       
#         while "#SECEND" not in line:
#             section.append(line)
#             lineIndex += 1
#             line = lines[lineIndex]
           
#         endIndex = lineIndex
       
#         newSection = section * len(info)
       
#         newIndex = 0
#         while newIndex < len(newSection):
           
#             if
               
       
#     lineIndex += 1

           
           
       

   
