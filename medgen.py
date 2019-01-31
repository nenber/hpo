# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 15:41:38 2019

@author: piedagnel
"""
import xlrd
from urllib2 import urlopen
import re
patt = re.compile("[^\t]+")
listGeneSymbol = []
listGenSymbolToHPO = [
listCores = []

uurl = 'http://compbio.charite.de/jenkins/job/hpo.annotations.monthly/lastSuccessfulBuild/artifact/annotation/ALL_SOURCES_ALL_FREQUENCIES_genes_to_phenotype.txt'


workbook = xlrd.open_workbook("//home//piedagnel//Desktop//667_genes_list_2019.xlsx")
worksheet = workbook.sheet_by_index(0)
listGeneSymbol = set(worksheet.col_values(0))






#FUNCTION
def download(t_url):
    response = urlopen(t_url)
    data = response.read()

    txt_str = str(data)
    lines = txt_str.splitlines()
    
    listGenSymbolToHPO = set(lines)
    

download(uurl)

for line in listGenSymbolToHPO:
    listCores.append(line.split())
print(listCores)



#input("")