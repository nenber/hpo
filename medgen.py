# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 15:41:38 2019

@author: piedagnel
"""
import xlrd
import re
import csv
patt = re.compile("[^\t]+")
listGeneSymbol = []
listGeneSymbolFromHpo = []
listDisease = []
listIdHpo = []
length = 0
listBaseGene = []
pathGene = "/home/piedagnel/Desktop/Medgen/ALL_SOURCES_ALL_FREQUENCIES_genes_to_phenotype.txt"
pathDisease = "/home/piedagnel/Desktop/Medgen/disease_names.txt"
uurl = 'http://compbio.charite.de/jenkins/job/hpo.annotations.monthly/lastSuccessfulBuild/artifact/annotation/ALL_SOURCES_ALL_FREQUENCIES_genes_to_phenotype.txt'

def getCommonID(listA = [],  listB = []):
    return list(set(listA) & set(listB))

def getmatching(lines, keywords):
    result = []
    keywords = set(keywords)
    for line in lines:
        matches = len(keywords & set(line.split()))
        if matches:
            result.append((matches, line))
    return (line for matches, line in sorted(result))
#FUNCTION
#def download(t_url):
#    """Download a .txt and return a list of all lines
#    """
#    response = urlopen(t_url)
#    data = response.read()
#
#    txt_str = str(data)
#    lines = txt_str.splitlines()

#RECUPERATION DES DATA DANS LES FICHIERS
workbook = xlrd.open_workbook("//home//piedagnel//Desktop//667_genes_list_2019.xlsx")
worksheet = workbook.sheet_by_index(0)
listGeneSymbol = worksheet.col_values(0)

fileGene = open(pathGene, 'r')
parcourGene = fileGene.readline()
while parcourGene:
    temp = parcourGene
    parcourGene = fileGene.readline()
    listGeneSymbolFromHpo.append(temp.split()[1])



commonGene = list(set(listGeneSymbolFromHpo) & set(listGeneSymbol))

with open(pathGene, 'rb') as csvfile:
     spamreader = csv.reader(csvfile, delimiter="\t", quotechar='|')
     i = 0
     for row in spamreader:
         try:
             if i > 0:
                 if row[1] in commonGene:
                     listIdHpo.append(row[3])
             else:
                 i = i + 1
         except IndexError as e:
             print("erreur a la ligne : ",row)
                 
             
#print(listIdHpo)








with open(pathDisease, 'rb') as csvfile:
     spamreader = csv.reader(csvfile, delimiter="\t", quotechar='|')
     i = 0
     for row in spamreader:
         try:
             if i > 1:
                 if row[3] in listIdHpo:
                     listDisease.append(row[0])
             else:
                 i = i + 1
         except IndexError as e:
             print("erreur a la ligne : ",row)
i = 0
for row in listDisease:
    print(row)
    i = i + 1
print("Maladies associes : ",i)


