# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 13:28:01 2019

@author: piedagnel
"""
import xlrd
import sys
sys.setrecursionlimit(10000)
Ancestors = []

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


def GetAncestors(hpo, rootDict):
    for description in rootDict:
        if description == "is_a":
            for parent in rootDict[description].split("|"):
                parent = parent.split("!")[0][:-1]
                Ancestors.append(parent)
                GetAncestors(parent, rootDict)
                break
        print Ancestors
        
        
def select_parents(rootDict,HPO):

    retour={}
    i=1
    
    while HPO!=0:
    
        print(HPO)
        #if rootDict[HPO]["is_a"]:
        if "is_a" in rootDict[HPO].keys():
            
            #print(rootDict[HPO].keys())
            
            if "!" in rootDict[HPO]["is_a"]:
            
                HPO_parent=rootDict[HPO]["is_a"].split("!")[0].replace(" ","")
                
                retour[HPO_parent]=i
                
                i+=1
                
            HPO=HPO_parent
                
        else:
            
            HPO=0
                


    return retour       
    
    
def select_parents_2(rootDict,HPO):

    retour={}
    i=1
    
    while HPO!=0:
    
        #if rootDict[HPO]["is_a"]:
        if "is_a" in rootDict[HPO].keys():
            
            #print(rootDict[HPO].keys())
            
            if "!" in rootDict[HPO]["is_a"]:
            
                HPO_parent=rootDict[HPO]["is_a"].split("!")[0].replace(" ","")
                
               
                
                retour[HPO_parent] = {"Level":i}
                
                i+=1
                
            HPO=HPO_parent
                
        else:
            HPO=0
    
    


    return retour
    
        
def main():
    
    rootDict = GetTreeObo_2("hp.obo")
    
    
    #print(rootDict.keys())
    
#    for HPO in rootDict:
#        
#        print(rootDict[HPO].keys())
    
#    print(select_parents_2(rootDict,"HP:0000509"))
    for key in rootDict:
        parents = select_parents_2(rootDict, key)
        rootDict[key]["Parents"] = parents
    
    for key in rootDict:
        print key + " : "        
        for subkey in rootDict[key]:
            print subkey + " : " + str(rootDict[key][subkey])
    
    
    
#    for "HP:0000509" in rootDict:
#        print rootDict['HP:0000509']["is_a"]
        
        
#
#    dictChildren = GetAllChildren(rootDict)
#    for key in dictChildren:
#        print key + " : " + str(dictChildren[key])
#        
#    
#    from networkx.readwrite import json_graph
#    G = nx.DiGraph([(1,2)])
#    data = json_graph.tree_data(G,root=1)
#    H = json_graph.tree_graph(data)


main()

