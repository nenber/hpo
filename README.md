# How to run
**From terminal :** ```python2 HpoFromGeneList.py -path [Input file] -ng [Amount of gene] -nd [Amount of disease]```
	
**Parameters**
* [Mandatory] -path : The path of the input file
    * *Exemple : ```-path '/home/user/Desktop/genes_list.xlsx'```*
    
* [Optional] -ng : Amount of Genes diplayed in the 5th column
    * *Exemple : ```-ng 5```*
    * *By default is 5*
    
* [Optional] -nd : Amount of Diseases displayed int the 8th column
    * *Exemple : ```-nd 5```*
    * *By default is 5*
# Examples of use
* **Example 1**
```pyton2 HpoFromGeneList.py -path '/home/user/Desktop/genes_list.xlsx'```
* **Example 2**
```pyton2 HpoFromGeneList.py -path '/home/user/Desktop/genes_list.xlsx' -ng 2```
 * **Example 3**
```pyton2 HpoFromGeneList.py -path '/home/user/Desktop/genes_lis.xlsx' -ng 2 -nd 6```
# Note
The script will automatically ignore the first row of the input file (this is usually an header) 

# Dependency
python 2
