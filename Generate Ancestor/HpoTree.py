# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 13:28:01 2019

@author: piedagnel
"""
import xlrd


def GetData(path):
    workbook = xlrd.open_workbook(path)
    worksheet = workbook.sheet_by_index(0)
    return worksheet.col_values(0)
    
def GetTreeObo(fi):
    f = open(fi)
    obo = f.readlines()
    tempKey = ""
    tempList = []
    dictHp = {}
    for line in obo[19:]:
        if line[:4] == "id: ":
            tempKey = line[4:]
        elif line != "\n" and line != "[Term]\n":
            elem = line[:len(line)-1]
            tempList.append(elem)
        elif line == "\n":
            dictHp[tempKey] = tempList
            tempList = []
    return dictHp
    
def GetTreeObo_2(fi):
    f = open(fi)
    obo = f.readlines()
    tempKey = ""
    tempDict = {}
    dictHp = {}
    for line in obo[19:]:        
        if line[:4] == "id: ":
            tempKey = line[4:].replace("\n","")
            
        elif line != "\n" and line != "[Term]\n":
            elem = line[:-1]
            separator = elem.index(":")
#           SI LA KEY EXISTE DEJA DANS LE DICTIONNAIRE
            if elem[:separator] in tempDict.keys():
                value = elem[separator+2:]
                
#               SI CETTE KEY EST "is_a"
                if line[:4] == "is_a":
                    tempDict[elem[:separator]] += ("|"+value)
                else:
                    tempDict[elem[:separator]] += value
            else:
                value = elem[separator+2:]
#                SI CETTE KEY EST "is_a"
                if line[:4] == "is_a":
                    tempDict[elem[:separator]] = value
                else:
                    tempDict[elem[:separator]] = value    
                    
            
            
        elif line == "\n":
                       
            dictHp[tempKey] = tempDict
            tempDict = {}
    f.close()
    return dictHp
       

def GetAllChildren(rootDict):
    dictChildren = {}    
    for key in rootDict:
        for subkey in rootDict[key]:
            if subkey == "is_a":
                parent = rootDict[key][subkey]
                nbParent = parent.split('|')
                for hpParent in nbParent:
                    hpParent = hpParent.split('!')[0][:-1]
                    if hpParent not in dictChildren.keys():
                        dictChildren[hpParent] = [key]
                    else:
                        dictChildren[hpParent].append(key)
    return dictChildren


def main():
    rootDict = GetTreeObo_2("hp.obo")
    for key in rootDict:
        print key + " : "
        for subkey in rootDict[key]:
            print subkey + " : " + rootDict[key][subkey]
        print '\n\n'
        

    dictChildren = GetAllChildren(rootDict)
    for key in dictChildren:
        print key + " : " + str(dictChildren[key])
        
    import networkx as nx
    G = nx.Graph()
        


main()

