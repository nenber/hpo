# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 15:41:38 2019

@author: berenger piedagnel
"""
import xlrd
import csv
import urllib2
import codecs
import xml.etree.ElementTree as ET
import sys  
import os
import argparse

reload(sys)  
sys.setdefaultencoding('utf8')
cwd = os.getcwd()
#path = "/home/piedagnel/Desktop/667_genes_list_2019.xlsx"
pathHPO = cwd + "/ALL_SOURCES_ALL_FREQUENCIES_genes_to_phenotype.txt"
pathOrphadata = cwd + "/fr_product4_HPO.xml"
dictNbTermByGene = {}

parser = argparse.ArgumentParser()
parser.add_argument("-path",action="store",dest='path',help="Input file (csv mendatory), Example : \'/home/user/Desktop/667_genes_list_2019.xlsx\'",required=True ,type=str)
parser.add_argument("-ng", action="store",dest='numberGene', help="Amount of genes displayed per row",type=int)
parser.add_argument("-nd", action="store",dest='numberDisease', help="Amount of diseases displayed per row",type=int)
args = parser.parse_args()
#print("Vous avez précisé X =", args.ng)

#RECUPERATION DES DATA DANS LE FICHIER DE LAURENT
def GetData(path):
    workbook = xlrd.open_workbook(path)
    worksheet = workbook.sheet_by_index(0)
    return worksheet.col_values(0)
    
#DOWNLOAD FILE FROM HPO
def DlDataFromHpo():
    print("downloading data from HPO...")
    response = urllib2.urlopen('http://compbio.charite.de/jenkins/job/hpo.annotations.monthly/lastSuccessfulBuild/artifact/annotation/ALL_SOURCES_ALL_FREQUENCIES_genes_to_phenotype.txt')
    data = response.read()
    print("Done\nWriting Hpo's data...")
    f = open(pathHPO,"w") 
 
    f.write(data) 
    print("Done")
     
    f.close()
    
def DlDataFromOrphadata():
    print("downloading data from Orphadata...")
    response = urllib2.urlopen('http://www.orphadata.org/data/xml/fr_product4_HPO.xml')
    data = response.read()
    print("Done\nWriting Orphadata's data...")
    f = open(pathOrphadata,"w") 
 
    f.write(data) 
    print("Done")
     
    f.close()
    
    
#RECUPERATION DES DATA DANS LE FICHIER GENE TO PHENOTYPES
def GetGeneSymbolFromHpo():
    listGene = []
    fileGene = open(pathHPO, 'r')
    parcourGene = fileGene.readline()
    while parcourGene:
        temp = parcourGene
        parcourGene = fileGene.readline()
        listGene.append(temp.split()[1])
    fileGene.close()        
        
    return listGene


#ASSOCIATION DES GENE SYMBOL PANEL  <==> FICHIER GENE TO PHENOTYPE
def GetCommonFromList(listGeneSymbolFromHpo,listGeneSymbol):
    return list(set(listGeneSymbolFromHpo) & set(listGeneSymbol))

def ExtractNonCommon(listBase, listCommon):
    listNotIn = []
    for elem in list(listBase):
        if elem not in list(listCommon):
            listNotIn.append(elem)
            
    f =  open("GeneNotInCommon.csv", "wb")
    c = csv.writer(f)
       
    c.writerow(["Genes"])
    for elem in listNotIn:
        c.writerow([elem])
    f.close()
    
#RECUPERATION DES ID HPO EN FONCTION DES GENES
def GetHpoIdsByGene(listGene):
    dictionnaire = {}
    listHp = []
    listPhenotype = []
    dictMerged = {}
    with open(pathHPO, 'rb') as csvfile:
     spamreader = csv.reader(csvfile, delimiter="\t", quotechar='|')     
#     POUR PASSER LE HEADER
     actualGene = (next(spamreader))
     actualGene = (next(spamreader))

     for row in spamreader:
         try:
#            SI LE GENE EST DANS NOTRE LISTE DE GENES COMMUN
             if row[1] in listGene:
                 if row[1] == actualGene:
                     listHp.append(row[3])
                     listPhenotype.append(row[2])
                 else:
                     for i in range(0,len(sorted(listHp))):
                         dictMerged[listHp[i]] = listPhenotype[i] 
                         dictionnaire[actualGene] = dictMerged
                     listHp = []
                     listPhenotype = []
                     dictMerged = {}
                     actualGene = row[1]
         except IndexError:
             print("erreur a la ligne : ",row)
    return dictionnaire
    
#def GetPercentGeneFromDict(dictionnaire):
#    totalgene = 0
#    dictPercentByGene = {}
#    for key in dictionnaire:
#        totalgene += len(dictionnaire[key])
#    for key in dictionnaire:
#        length = len(dictionnaire[key])
#        dictPercentByGene[key] = (float(length)/float(totalgene))*float(100)
#    for key, value in sorted(dictPercentByGene.items(), key = lambda x: x[1], reverse = True):
#        dictPercentByGene.update({key : value})
#    return dictPercentByGene
    
def CountHPO(dictHpo, nbGene):
    nbTotal = 0
    dictNbHpoByGene = {}
    dictNbGeneByHpo = {}
    dictTermByHpoId = {}
    dictGeneByHpo = {}
    listGene = []
    for gene in dictHpo:
        if gene not in dictNbHpoByGene:    
            dictNbHpoByGene[gene] = 0
        dictNbHpoByGene[gene] += len(dictHpo[gene])
        nbTotal += len(dictHpo[gene])
        listHpo = dictHpo[gene].keys()
        for hpoLine in listHpo:
            if hpoLine not in dictNbGeneByHpo:
                dictNbGeneByHpo[hpoLine] = {}
            if gene not in dictNbGeneByHpo[hpoLine].keys():
                dictNbGeneByHpo[hpoLine][gene] = 0
            dictNbGeneByHpo[hpoLine][gene] += 1
            if hpoLine not in dictTermByHpoId:
                dictTermByHpoId[hpoLine] = ""
            dictTermByHpoId[hpoLine] = dictHpo[gene][hpoLine]        
            i = 0
            listGene = []        
            for g in dictHpo.keys():
                if nbGene == 0:
                    if hpoLine in dictHpo[g].keys() and hpoLine not in listGene:
                        listGene.append(g)
                        i += 1
                elif nbGene > 0:
#                    if i == nbGene or i > nbGene:
#                        break
                    if hpoLine in dictHpo[g].keys() and hpoLine not in listGene:
                        listGene.append(g)
                        i += 1
            dictGeneByHpo[hpoLine] = listGene
    return dictNbHpoByGene, nbTotal, dictNbGeneByHpo, dictTermByHpoId, dictGeneByHpo

def ParseTree(nbDisease):
    dictDisease = {}
    tree = ET.parse("fr_product4_HPO.xml")
    root = tree.getroot()    
    for disorder in root[1]:
        for name in disorder.findall("Name"):
            listTemp = []
            for hpo in disorder.iter("HPOId"):
                listTemp.append(hpo.text)
            dictDisease[name.text] = listTemp
    return dictDisease

    

def main():
    if args.numberGene:
        nbGeneByHpoDesired = args.numberGene
    else:
        nbGeneByHpoDesired = 5
    if args.numberDisease:
        nbDiseaseDesired = args.numberDisease
    else:
        nbDiseaseDesired = 5
    if args.path:
        path = args.path
    
    DlDataFromHpo()
    DlDataFromOrphadata()    
    print("Generating \"result_HPO.csv\"..."   ) 
    listGeneSymbol = GetData(path)
    listGeneSymbolHpo = GetGeneSymbolFromHpo()
    commonGenes = GetCommonFromList(listGeneSymbol,listGeneSymbolHpo) 
    HpoIds = GetHpoIdsByGene(commonGenes)
    dictTemp, nbTotal, dictNbGeneByHpo, dictTermByHpo, dictGeneByHpo = CountHPO(HpoIds,nbGeneByHpoDesired)
    dictDisease = ParseTree(6)
    
    
    cIdHp = ""
    cNbHp = ""
    cPercentHp = ""
    cNbGeneAssociated = ""
    term = ""
    globalDict = {}
    
    
#    POUR CHAQUE HPO DANS CHAQUE GENE
    for HPO in dictNbGeneByHpo:
        cIdHp = HPO
        cNbHp = len(dictNbGeneByHpo[HPO])
        cPercentHp = (float(cNbHp)/float(nbTotal)*float(100))
        cNbDiseaseAssociated = 0
        cDiseasesAssociated = ""
        cDiseasesAssociated1 = ""
        
#        POUR CHAQUE HPO CONTENU DANS CHAQUE MALADIE
        for k,v in dictDisease.items():
            if HPO in v:
                if cNbDiseaseAssociated < nbDiseaseDesired:
                    cDiseasesAssociated += k + " | "
                cDiseasesAssociated1 += k + " | "
                cNbDiseaseAssociated += 1
        cDiseasesAssociated = cDiseasesAssociated[:-1]
        cDiseasesAssociated = cDiseasesAssociated[:-1]
        cDiseasesAssociated1 = cDiseasesAssociated1[:-1]
        cDiseasesAssociated1 = cDiseasesAssociated1[:-1]
        if cNbDiseaseAssociated > nbDiseaseDesired:
            cDiseasesAssociated += "..."
        
#        POUR CHAQUE GENE 
        for gene in dictNbGeneByHpo[HPO]:
            cNbGeneAssociated = len(dictNbGeneByHpo[HPO])
            term = dictTermByHpo[HPO]
        cGenesAssociated = ""
        cGenesAssociated1 = ""
        i = 1
        for value in dictGeneByHpo[HPO]:
            if i <= nbGeneByHpoDesired :
                cGenesAssociated += value + " | "
            cGenesAssociated1 += value + " | "
            i += 1
        cGenesAssociated = cGenesAssociated[:-1]
        cGenesAssociated = cGenesAssociated[:-1]
        cGenesAssociated1 = cGenesAssociated1[:-1]
        cGenesAssociated1 = cGenesAssociated1[:-1]
        if cNbGeneAssociated > nbGeneByHpoDesired:
            cGenesAssociated += "..."
        globalDict[HPO] = [cIdHp,cNbHp,str(cPercentHp) + "%",term,cNbGeneAssociated,cGenesAssociated,cGenesAssociated1,cNbDiseaseAssociated,cDiseasesAssociated,cDiseasesAssociated1]
#        ISO-8859-1
    f = codecs.open("result_HPO.csv", "w",encoding="utf_8")
    c = csv.writer(f)
    c.writerow(["ID HPO","Nombre total","Pourcentage","Libellé", "Nombre de gene associés", str(nbGeneByHpoDesired) + " premiers Genes","Tous les Genes","Nombre de présence dans les maladies", str(nbDiseaseDesired) + " premiers maladies associés", "Toutes les maladies associés"])
    for key in globalDict:
        c.writerow(globalDict[key])
    f.close()
    
    ExtractNonCommon(listGeneSymbol,commonGenes)
    print("Done")
    print("\nNote : Common HPOs not found are written in the file \"GeneNotInCommon.csv\"\n")
main()





