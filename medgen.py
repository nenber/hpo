# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 15:41:38 2019

@author: piedagnel
"""
import xlrd
import csv
import operator

pathGene = "/home/piedagnel/Desktop/Medgen/ALL_SOURCES_ALL_FREQUENCIES_genes_to_phenotype.txt"
pathDisease = "/home/piedagnel/Desktop/Medgen/disease_names.txt"
uurl = 'http://compbio.charite.de/jenkins/job/hpo.annotations.monthly/lastSuccessfulBuild/artifact/annotation/ALL_SOURCES_ALL_FREQUENCIES_genes_to_phenotype.txt'
path = "//home//piedagnel//Desktop//667_genes_list_2019.xlsx"
dictNbTermByGene = {}

#RECUPERATION DES DATA DANS LE FICHIER DE LAURENT
def GetData(path):
    workbook = xlrd.open_workbook(path)
    worksheet = workbook.sheet_by_index(0)
    return worksheet.col_values(0)
    


#RECUPERATION DES DATA DANS LE FICHIER GENE TO PHENOTYPES
def GetGeneSymbolFromHpo():
    listGene = []
    fileGene = open(pathGene, 'r')
    parcourGene = fileGene.readline()
    while parcourGene:
        temp = parcourGene
        parcourGene = fileGene.readline()
        listGene.append(temp.split()[1])
        
    fileGene.close()        
        
    return listGene


#ASSOCIATION DES GENE SYMBOL PANEL LAURENT <==> FICHIER GENE TO PHENOTYPE
def GetCommonFromList(listGeneSymbolFromHpo,listGeneSymbol):
    return list(set(listGeneSymbolFromHpo) & set(listGeneSymbol))


#RECUPERATION DES ID HPO EN FONCTION DES GENES
def GetHpoIdsByGene(listGene):
    dictionnaire = {}
    listHp = []
    listPhenotype = []
    dictMerged = {}
    with open(pathGene, 'rb') as csvfile:
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
    
def GetPercentGeneFromDict(dictionnaire):
    totalgene = 0
    dictPercentByGene = {}
    for key in dictionnaire:
        print"\n\n\n"
        print len(dictionnaire[key])
        totalgene += len(dictionnaire[key])
        print "========= " + key + " ========="
        print"\n"
        for subKey in dictionnaire[key]:
            print subKey + "  ==>  " + dictionnaire[key][subKey]
    for key in dictionnaire:
        length = len(dictionnaire[key])
        dictPercentByGene[key] = (float(length)/float(totalgene))*float(100)
    print len(dictionnaire.items())
    print totalgene
    for key, value in sorted(dictPercentByGene.items(), key = lambda x: x[1], reverse = True):
        dictPercentByGene.update({key : value})
    return dictPercentByGene
    
def GetAmountByHpoIds(dic):
    dictHPO = {}
#    POUR CHAQUE GENE
    for key in dic:
        hpoKey = dic[key]
        i = 0
#        POUR CHAQUE HPO ID
        for hpo in hpoKey:
            if(hpo in dictHPO):
                dictHPO[hpo] = dictHPO[hpo] + 1
            else:
                dictHPO[hpo] = 1
            
       # Create a list of tuples sorted by index 1 i.e. value field     
    dictHPO = sorted(dictHPO.items() ,reverse=True,  key=lambda x: x[1])
    return dictHPO
    

def main():
    listGeneSymbol = GetData(path)
    listGeneSymbolHpo = GetGeneSymbolFromHpo()
    commonGenes = GetCommonFromList(listGeneSymbol,listGeneSymbolHpo) 
    HpoIds = GetHpoIdsByGene(commonGenes)
    DictPercent = GetPercentGeneFromDict(HpoIds)
    AmountHPO = GetAmountByHpoIds(HpoIds)

    c = csv.writer(open("Iteration_HPO.csv", "wb"))
    c.writerow(["ID HPO","Nombre d'apparition","Pourcentage"])
    tot = 0
    for elem in AmountHPO:
        tot += elem[1]
    for elem in AmountHPO :
        c.writerow([elem[0],elem[1], (float(elem[1])/float(tot))*float(100)]) 
    for elem in DictPercent:
        print elem + " : " + str(DictPercent[elem])
            
main()





