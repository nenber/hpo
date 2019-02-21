# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 15:41:38 2019

@author: piedagnel
"""
import xlrd
import csv
import urllib2
from xml.dom import minidom

pathHPO = "/home/piedagnel/Desktop/Medgen/ALL_SOURCES_ALL_FREQUENCIES_genes_to_phenotype.txt"
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
    f = open(pathHPO,"w") 
 
    f.write(data) 
    print "Done"
     
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
    temp = []
#    print dic.values()[0].keys()
    for gene in dic:
        for hp in dic[gene]:
            temp.append(hp)
    
    for line in temp:
        amount = temp.count(line)
        dictHPO[line] = amount

            
    # Create a list of tuples sorted by index 1 i.e. value field     
    dictHPO = dict(sorted(dictHPO.items() ,reverse=True,  key=lambda x: x[1]))
    return dictHPO
    
    
def CountHPO(dictHpo):
    nbTotal = 0
    dictNbHpoByGene = {}
    dictNbGeneByHpo = {}
    dictTermByHpoId = {}
    dict5GeneByHpo = {}
    list5Gene = []
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
            list5Gene = []
            
            for g in dictHpo.keys():
                if i == 5 or i > 5:
                    break
                if hpoLine in dictHpo[g].keys() and hpoLine not in list5Gene:
                    list5Gene.append(g)
                    i += 1
                    
                 
            
            dict5GeneByHpo[hpoLine] = list5Gene
    return dictNbHpoByGene, nbTotal, dictNbGeneByHpo, dictTermByHpoId, dict5GeneByHpo

def main():
#    DlDataFromHpo()
#    listGeneSymbol = GetData(path)
#    listGeneSymbolHpo = GetGeneSymbolFromHpo()
#    commonGenes = GetCommonFromList(listGeneSymbol,listGeneSymbolHpo) 
#    HpoIds = GetHpoIdsByGene(commonGenes)
#    AmountHPO = GetAmountByHpoIds(HpoIds)
#    
#    dictTemp, nbTotal, dictNbGeneByHpo, dictTermByHpo, dict5GeneByHpo = CountHPO(HpoIds)
#    #print dictNbGeneByHpo
#
#
#    cIdHp = ""
#    cNbHp = ""
#    cPercentHp = ""
#    cNbGeneAssociated = ""
#    term = ""
#    globalDict = {}
#
#    for HPO in dictNbGeneByHpo:
#        cIdHp = HPO
#        cNbHp = len(dictNbGeneByHpo[HPO])
##        cPercentHp = (float(cNbHp)/float(len(AmountHPO)))*float(100)
#        cPercentHp = (float(cNbHp)/float(nbTotal)*float(100))
##        dictNbGeneByHpo[HPO] = dictNbGeneByHpo[HPO]
#        for gene in dictNbGeneByHpo[HPO]:
#            cNbGeneAssociated = len(dictNbGeneByHpo[HPO])
#            term = dictTermByHpo[HPO]
#        s = ""
#        for value in dict5GeneByHpo[HPO]:
#            s += value + ", "
#        s = s[:-1]
#        s = s[:-1]
#        s += "..."
#        globalDict[HPO] = [cIdHp,cNbHp,cPercentHp,term,cNbGeneAssociated,s]
#        
#    f = open("result_HPO.csv", "wb")
#    c = csv.writer(f)
#    c.writerow(["ID HPO","Nombre total","Pourcentage","Libellé", "Nombre de gene associé (a ce hp)", "Genes","Nombre de présence dans les maladies"])
#    for key in globalDict:
#        c.writerow(globalDict[key])
#    f.close()
    
#    XML
    doc = minidom.parse('fr_product4_HPO_status.xml')
    root = doc.documentElement
    for element in root.getElementsByTagName('Disorder'):
        attrs   = element.attributes
        urlnode = attrs['id']
        print "Disorder id : " + urlnode.nodeValue


#    ExtractNonCommon(listGeneSymbol,commonGenes)
main()





