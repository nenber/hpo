# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 15:41:38 2019

@author: piedagnel
"""
import xlrd
import csv
import urllib2

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
    
#DOWNLOAD FILE FROM HPO
def DlDataFromHpo():
    print "downloading data from HPO..."
    response = urllib2.urlopen('http://compbio.charite.de/jenkins/job/hpo.annotations.monthly/lastSuccessfulBuild/artifact/annotation/ALL_SOURCES_ALL_FREQUENCIES_genes_to_phenotype.txt')
    data = response.read()
    print "Done\nWriting Hpo's data..."
    print "Writing Hpo's data..."
    f = open(pathGene,"w") 
 
    f.write(data) 
    print "Done"
     
    f.close() 
    
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
        totalgene += len(dictionnaire[key])
    for key in dictionnaire:
        length = len(dictionnaire[key])
        dictPercentByGene[key] = (float(length)/float(totalgene))*float(100)
    for key, value in sorted(dictPercentByGene.items(), key = lambda x: x[1], reverse = True):
        dictPercentByGene.update({key : value})
    return dictPercentByGene
    
def GetAmountByHpoIds(dic):
    dictHPO = {}
#    POUR CHAQUE GENE
    for key in dic:
        hpoKey = dic[key]
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
    DlDataFromHpo()
    listGeneSymbol = GetData(path)
    listGeneSymbolHpo = GetGeneSymbolFromHpo()
    commonGenes = GetCommonFromList(listGeneSymbol,listGeneSymbolHpo) 
    HpoIds = GetHpoIdsByGene(commonGenes)
    AmountHPO = GetAmountByHpoIds(HpoIds)
    
    tempDic = {}
    for dic in HpoIds:
        tempDic.update(HpoIds[dic].items())
    f = open("Iteration_HPO.csv", "wb")
    c = csv.writer(f)
    c.writerow(["ID HPO","Nombre d'apparition","Pourcentage","Libellé"])
    tot = 0
    libelle = ""
    for elem in AmountHPO:
        tot += elem[1]
    
    
    for elem in AmountHPO :
#        CE FOR SERT JUSTE A RECUPERER LE SYMPTOME
        for liste in HpoIds.values():
            for hp in liste:
                if elem[0] == hp:
                    libelle = liste[hp]
        c.writerow([elem[0],elem[1], (float(elem[1])/float(tot))*float(100),libelle])
    f.close()
    
    f =  open("NbHpByGene.csv", "wb")
    c = csv.writer(f)
       
    c.writerow(["Genes","Nombre de gene"])
    for elem in HpoIds:
        gene = elem
        count = 0
        for i in elem:
            count += 1
        c.writerow([gene,count])
    f.close()
    
    ExtractNonCommon(listGeneSymbol,commonGenes)
main()





