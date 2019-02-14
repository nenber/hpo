# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 15:41:38 2019

@author: piedagnel
"""
import xlrd
import csv
import urllib2

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
    temp = 0
#    POUR CHAQUE GENE
    for key in dic:
        hpoKey = dic[key]
#        POUR CHAQUE HPO ID
        for hpo in hpoKey:
                
            for gene in dic:
                try:
                    for hp in dic[gene]:
                        if hp == hpo:
                            temp += 1
                except:
                    print "erreur"
            dictHPO[hpo] = temp
            temp = 0
       # Create a list of tuples sorted by index 1 i.e. value field     
    dictHPO = dict(sorted(dictHPO.items() ,reverse=True,  key=lambda x: x[1]))
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
    c.writerow(["ID HPO","Nombre d'apparition","Pourcentage","Libellé", "Nombre de gene associé (a ce hp)", "Nombre de présence dans les maladies","Genes"])
    globalDict = {}
#    cIdHp, cNbHp, cPercentHp, cTerm, cNbGene, Genes, cNbDiseaseAssociated
    cIdHp = ""
    cNbHp = ""
    cPercentHp = ""
    cNbGeneAssociated = 0
#   ECRITURE DES ROWS
    for gene in HpoIds:
        hps = HpoIds[gene]
        for hp in hps:
            term = hps[hp]
            cIdHp = hp
            cNbGeneAssociated = 0
            for key in AmountHPO:
                if key == cIdHp:
                    cNbHp = AmountHPO[key]
                    cPercentHp = (float(cNbHp)/float(len(AmountHPO)))*float(100)
            
            for key in HpoIds: 
                for subKey in HpoIds[key]:
                    if subKey == cIdHp:
                        cNbGeneAssociated += 1
                        break
                
                 
            globalDict[hp] = [cIdHp,cNbHp,cPercentHp,term,str(cNbGeneAssociated)]
    f = open("Iteration_HPO.csv", "wb")
    c = csv.writer(f)
    c.writerow(["ID HPO","Nombre d'apparition","Pourcentage","Libellé", "Nombre de gene associé (a ce hp)", "Nombre de présence dans les maladies","Genes"])
    for key in globalDict:
        c.writerow(globalDict[key])
    f.close()
    
    

    
    
    
    
#    TOTAL D'ID HPO
#    for elem in AmountHPO:
#        tot += elem[1]
#    
#    for elem in AmountHPO :
##        CE FOR SERT JUSTE A RECUPERER LE SYMPTOME
#        for liste in HpoIds.values():
#            for hp in liste:
#                if elem[0] == hp:
#                    libelle = liste[hp]
#        c.writerow([elem[0],elem[1], (float(elem[1])/float(tot))*float(100),libelle])
#    f.close()
    
    
    
    
    
    
    
    
    
    
    
#    f =  open("NbHpByGene.csv", "wb")
#    c = csv.writer(f)
#       
#    c.writerow(["Genes","Nombre de gene"])
#    for elem in HpoIds:
#        gene = elem
#        count = 0
#        for i in elem:
#            count += 1
#        c.writerow([gene,count])
#    f.close()
    
    ExtractNonCommon(listGeneSymbol,commonGenes)
main()





