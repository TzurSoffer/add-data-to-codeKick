import json
import difflib
import pyjsonviewer

def getObjectData(function, terms=["def", "class"], posiblePrefixes = ["-c", "-d", "-n", "-t"]) -> dict:
    """_summary_
        find the name of any function or class
    Args:
        str function: the function
        str termPos: the end pos of "def" or "class"

    Returns:
        dict: object data
    """
    prefixes  = []
    newData = {}
    i = 1
    for prefix in posiblePrefixes:
        prefixPos = function.find(prefix)
        if prefixPos != -1:
            
            startPos = prefixPos+len(prefix)+1
            while i< len(posiblePrefixes):
                endPos = function.find(posiblePrefixes[i])
                if endPos != -1:
                    newData[prefix] = function[startPos:endPos]
                    break
                i += 1

            else:
                newData[prefix] = function[startPos:]
            i+=1

    return(newData)

def removeDuplicates(l, by = "data"):
    temp = []
    res = []
    for dictionary in l:
        val = dictionary[by]
        if val not in temp:
            temp.append(val)
            res.append(dictionary)
    return(res)

if __name__ == "__main__":
    filesData = []
    with open("dataMathOrganized.json", "r") as f:
        filesData.append(json.load(f))
    with open("dataDefOrganized.json", "r") as f:
        filesData.append(json.load(f))
    with open("dataMatrixOrganized.json", "r") as f:
        filesData.append(json.load(f))
    with open("dataSympyOrganized.json", "r") as f:
        filesData.append(json.load(f))
    with open("dataApiOrganized.json", "r") as f:
        filesData.append(json.load(f))
    with open("dataNumpyOrganized.json", "r") as f:
        filesData.append(json.load(f))
    with open("dataPandasOrganized.json", "r") as f:
        filesData.append(json.load(f))

        #print(dataMath[:10])

    print("class findPrimes:")
    sm = difflib.SequenceMatcher(None)
    while True:
        data = []
        inputData = input(">>>")
        inputData = getObjectData(inputData)
        if "-n" in inputData:
            sm.set_seq1(inputData["-n"].replace(" ", "_"))
            print(inputData["-n"].replace(" ", "_"))
        
        elif "-d" in inputData:
            #print(inputData["-d"])
            sm.set_seq1(inputData["-d"])
        
        else:
            continue
        print(inputData)
        
        for file in filesData:
            for funcs in file:
                for d in funcs:
                    if "-c" in inputData:
                        if d["category"] == inputData["-c"].replace(" ", ""):
                            pass
                        else:
                            continue

                    if "-t" in inputData:
                        if d["term"] == inputData["-t"].replace(" ", ""):
                            pass
                        else:
                            continue

                    if "-n" in inputData:
                        sm.set_seq2(d["name"].replace(" ", ""))
                        print(d["name"].replace(" ", ""))
                    
                    elif "-d" in inputData:
                        if d["description"] == None:
                            continue
                        sm.set_seq2(d["description"])
                    acuracy = sm.ratio()*100
                    #print(acuracy)
                    d["acuracy"] = acuracy
                    data.append(d)

        sortedData = removeDuplicates(sorted(data, key=lambda d: d['acuracy'], reverse=True))

    #> search by description
    ## add search by catagory
    # interface to add object to dict
    # find import for object   
        

        #pyjsonviewer.view_data(json_file="dat/list.json")
        #jsonViewer = JsonViewer.MyApp(data1=sortedData[:11])
        #jsonViewer.MainLoop()
        #pyjsonviewer.view_data(json_data=sortedData[:11])
        #print(sortedData[0])
