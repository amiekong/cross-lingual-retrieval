import os
import string
import re
from nltk.stem import *
import itertools
import sys
import webbrowser
# Name: Amie Kong
# Description: This python file parses the .txt data from the Medical Spanish-English Parallel
# Corpora (https://zenodo.org/record/3562536). 6110 documents from the Spanish dataset was collected
# and 5047 English documents were collected. The program combines all of the .txt files and
# returns an .xml file used to add the documents to the Solr CLIR core.
def read_data(dir):
    text = []
    count = 0
    for filename in os.listdir(dir):
        if filename.endswith('.txt'):
            content = []
            count += 1
            with open(str(dir + filename), 'r') as file:
                title = file.readline()
            with open(str(dir + filename), 'r') as file:
                next(file)
                for line in file:
                    body_text = file.read().replace('\n', '')
                    body_text = body_text.replace('P ', '')
                    body_text = body_text.replace('T ', '')
                    body_text = body_text.replace('&', '')
                    #removing invalid XML characters
                    body_text = body_text.replace('<', '')
                    body_text = body_text.replace('>', '')
                    body_text = body_text.replace('"', '')
                    body_text = body_text.replace("'", '')
            text.append((str(title), (str(body_text))))
    print(count)
    return text


#main method
args = sys.argv

data = read_data(args[1])

# generates an xml file to add documents to solr
itemlist = []
itemlist.append('<add>')
count = 5048
for item in data:
    itemlist.append('<doc><field name="id">' + str(count) + '</field> <field name="title_es">' + str(item[0]) + '</field> <field name="text_es">' + str(item[1]) + '</field></doc>')
    count += 1
itemlist.append('</add>')

with open('docs_es.xml', "w") as outfile:
    outfile.write("\n".join(str(item) for item in itemlist))

# generates queries to solr
#print(preprocessed_queries)
