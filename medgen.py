# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 15:41:38 2019

@author: piedagnel
"""
import xlrd
import csv
pathGene = "/home/piedagnel/Desktop/Medgen/ALL_SOURCES_ALL_FREQUENCIES_genes_to_phenotype.txt"
pathDisease = "/home/piedagnel/Desktop/Medgen/disease_names.txt"
uurl = 'http://compbio.charite.de/jenkins/job/hpo.annotations.monthly/lastSuccessfulBuild/artifact/annotation/ALL_SOURCES_ALL_FREQUENCIES_genes_to_phenotype.txt'
path = "//home//piedagnel//Desktop//667_genes_list_2019.xlsx"

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
    
#RECUPERATION DES DISEASE NAME EN FONCTION DES ID HPO
def GetDiseaseFromIdsHpo(dictHpo):
    with open(pathDisease, 'rb') as csvfile:
         dictionnaire = {}
         spamreader = csv.reader(csvfile, delimiter="\t", quotechar='|')
         actualRow = (next(spamreader))
         actualRow = (next(spamreader))         
         try:
             for key in dictHpo:
                 a = ""
         except IndexError:
             print ""
    return dictionnaire

def main():
    listGeneSymbol = GetData(path)
    listGeneSymbolHpo = GetGeneSymbolFromHpo()
    commonGenes = GetCommonFromList(listGeneSymbol,listGeneSymbolHpo) 
    HpoIds = GetHpoIdsByGene(commonGenes)
    dictDisease = GetDiseaseFromIdsHpo(HpoIds)  
    
    
    #AFFICHAGE DES HPO ID + PHENOTYPES
    i = 0
    for key in HpoIds:
        print"\n\n\n"
        print "========= " + key + " ========="
        print"\n"
        for subKey in HpoIds[key]:
            print subKey + "  ==>  " + HpoIds[key][subKey]
    #print "Value : %s" %  HpoIds.get('CLPP')
    print "\n" + "Maladies associes : "+ str(i)
    print "\n"
    print len(HpoIds.items())
main()




