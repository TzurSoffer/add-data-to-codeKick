import json

class FindObjectInText():
    """
    A class that automates the process of seperating files to objects
    """
    def __init__(self, text, category, objIndex = 0, termsToFind = ["class ", "def "]):
        self.objIndex = objIndex
        self.termsToFind = termsToFind
        self.objectPosInText = 0

        self.data = {}
        self.FinalData = {}

        self.text = text.replace("    ", "\t")
        self.lines = self.text.split("\n")
        self.textLength = len(self.text)
        
        self.category = category
    
    def _findIndentetion(self, line) -> int:
        """_summary_

        Args:
            str line: line you want to find indentetion (using "\t")
        
        Returns:
            int: indentetion level
        """
        indentetion = 0
        while indentetion < len(line):
            if line[indentetion] == "\t":
                indentetion += 1
            else:
                break

        return(indentetion)
    
    def _findImports(self) -> list:
        """get all the imports in code

        Args:
            None

        Returns:
            list: the lines of the imports
        """
        
        imports = []
        for line in self.lines:
            if "import" in line:
                imports.append(line)
        return(imports)

    def _getObjectName(self, function, termPos) -> str:
        """_summary_
            find the name of any function or class
        Args:
            str function: the function
            str termPos: the end pos of "def" or "class"

        Returns:
            str: name of object
        """
        objName = function.replace(" ", "").split("\n")[0]
        
        objOpenparenthesis = objName.find("(")
        objColumn = function.find(":")
        
        if objOpenparenthesis != -1:
            objName = objName[termPos:objOpenparenthesis]
        
        elif objColumn != -1:
            if(objOpenparenthesis > objColumn):
                objName = objName[termPos:objColumn]
                
        return(objName)

    def _findTermEnd(self, data) -> dict:
        """edits a dictionary and add the ending pos of an object

        Args:
            dict data: the dictionary with "firstLine" and "indentetion"

        Returns:
            dict
        """
        firstLine = data["firstLine"]
        indentetion = data["indentetion"]
        data["lastLine"] = len(self.lines)-1
        
        for i, line in enumerate(self.lines[firstLine+1:]):
            lineIndentetion = self._findIndentetion(line)
            if(line.strip() != "" and lineIndentetion <= indentetion):
                data["lastLine"] = firstLine+i
                break
        
        return(data["lastLine"])
    
    def _combineData(self, data) -> str:
        """return the text of an object

        Args:
            dict data: a dictionary containing the "firstLine" and "lastLine" of the object

        Returns:
            str: the text of an object
        """
        
        firstLine = data["firstLine"]
        lastLine = data["lastLine"]
        
        lines = ""
        for line in self.lines[firstLine:lastLine]:
            lines += line+"\n"
        
        return(lines)
    
    def _findDescription(self, text):
        desc = text.split('"""')
        if len(desc) > 1:
            desc = desc[1]
        else:
            desc = None
        return(desc)

    def findTerms(self, saveData = True) -> dict:
        """returns a dictionary with all the objects and their names

        Args:
            saveData (bool, optional): Defaults to True.

        Returns:
            dict: a dictionary with all the objects and their names
        """
        data = []
        newData = []
        currentLine = 0

        while currentLine < len(self.lines): #< loop through all the lines in the text
            line = self.lines[currentLine]
            for term in self.termsToFind:
                termPos = line.find(term)
                if termPos != -1:
                    indentetion = self._findIndentetion(line)
                    stripedTerm = term.replace(" ", "")
                    
                    #create the necesary data to find functions/classes:
                    dataDict = {
                        "firstLine":currentLine,
                         "term":stripedTerm,
                         "indentetion":indentetion,
                        }
                    dataDict["lastLine"] = self._findTermEnd(dataDict)
                    data.append(dataDict)
                    
                    #get the functions out of our text:
                    dataCombined = self._combineData(dataDict)
                    description = self._findDescription(dataCombined)
                    
                    
                    if dataCombined.strip() != "": #< we dont want any empy functions or classes in our data
                        name = self._getObjectName(dataCombined, len(stripedTerm))

                        newData.append({
                            "term": stripedTerm,
                            "name": name,
                            "data": dataCombined,
                            "description": description,
                            "category": self.category,
                            "imports": self._findImports()
                            })
                    
                    currentLine = data[len(data)-1]["lastLine"]

            currentLine += 1
            
        if saveData == True:
            self.data = data
            self.newData = newData

        return(newData)


if __name__ == "__main__":
    import pyjsonviewer
    
    name = "dataSympy"
    with open(name+".json", "r") as f:
        jsonFile = json.load(f)

    data = []
    for i in jsonFile:
        text = jsonFile[i]
        objectFinder = FindObjectInText(text, "math")
        data.append(objectFinder.findTerms())

        
    with open(name+"Organized.json", "w") as f:
        json.dump(data, f)
    print(len(str(data)))
    pyjsonviewer.view_data(json_data=data)
