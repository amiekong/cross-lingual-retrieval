## Implementing an English-Spanish Cross-Lingual Information Retrieval System With Topic Model Query Expansion

Implemented a Cross-Lingual Information Retrieval System for English-Spanish where the returned
results are in the specified target language regardless of the query’s source language. When a 
user enters an English query and wants to filter it to Spanish results it will only
return Spanish results. The user can type an English or Spanish query and have the option to filter it to
“return Spanish results” or “return Spanish results”. The results returned will return a list of Spanish or
English documents with the document title followed by the document text when the query is translated
and indexed against the dataset. By extracting latent topic information from the returned target
documents, an automatic query expansion feature will be enabled to reformulate a new query by
adding an extra term or two in an attempt to improve the relevance ranking of the relevant documents
retrieved if the precision of the results were low.

## Parallel Corpora Dataset
A subset of the Medical Spanish-English Corpora (MeSpEn) that was presented at the LREC
2018 Workshop MultilingualBIO: Multilingual Biomedical Text Processing was used which
contains aggregations of datasets from multiple sources such as IBECS, SciELO, Pubmed and
MedlinePlus. Consisting of health related documents in Spanish and English, MeSpEn is useful
for building parallel corpora for training and evaluating Spanish-English medical machine
translation systems, as well as generating multilingual automatic term extraction tools. The data
set includes Spanish and Latin American biomedical and clinical literature along with content
with information about diseases, conditions, and wellness issues for patients [1].
Specifically, the data set used for this project was MedlinePlus in TEI format, consisting of clean
raw text and XML files of each article, structured by sections and paragraphs on topics limited to
diseases, illnesses, symptoms, injuries, surgeries, health conditions, wellness issues, drugs herbs
and supplements. The raw text of 11,157 articles in English and Spanish were collected and
imported into the Solr instance using a Python program (combiner.py) that serves to combine the
text files into two separate XML files (English documents and Spanish documents) that will be
used to add the documents to the Solr instance [2].

## Implementing a Cross-Language Information Retrieval System (CLIR)
Accepting questions in one language (in this case English) and retrieving information in a
different language (e.g. Spanish) defines CLIR. There are two different approaches to handle
CLIR: translate the source language query into the target language and then retrieve the
documents (query translation) or translate the entire corpora in the source language and then
perform the retrieval (document translation); however, the second option requires a lot of
resources and time so the first approach of query translation will be used. Translational
ambiguity is expected in query translation, especially for short query text due to the limited
context. After translation is done, the task is then reduced into a monolingual IR task [4].

## Handling Multiple Languages in a Single Index
To handle multiple languages in the Solr core instance, two separate fields for Spanish and
English text (“text_en” and “text_es”) were included in the managed_schema file, along with the
field types and appropriate Stemmers for Spanish and English [6].

## Query Translation
A Python tool (deep-translator) that uses multiple translators was installed to translate the detected
source language of the query to the target language. The translated query was then used to search against
the Solr instance.

## Pseudo-Relevance Feedback: Query Expansion Based On Topic Distributions of Retrieved Documents
Using pseudo-relevance feedback (PRF), the user’s new formulated query will be based on the
top-ranked retrieved documents in the first retrieval round. Terms will be extracted to enhance the user’s
requirement from the top-ranked documents in the first retrieval round and then expand a query used in
the next retrieval round. PRF has shown an increase in retrieval performance by several studies [7]. A
Latent Dirichlet Allocation Topic Model from scikit, along with preprocessing and tokenization of the
retrieved documents was used to create a bag-of-words model and perform topic distribution of the top
retrieved documents and a new query was reevaluated in the final round of ranking (lda.py).

## Ranking Using Solr-Lucene
A similarity model using the built-in TF-IDF scoring algorithm in Lucene was used to give relevance
scores to each document in the search result and rank the documents.
