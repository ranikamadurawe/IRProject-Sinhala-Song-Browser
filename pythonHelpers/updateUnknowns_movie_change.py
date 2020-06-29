# This script is used to change any songs with no movies and or unknown keys and bests from the incosistent format to a consistent format of an index
# The chosen format was to apply "නොදන්‌නා" for keys and beats and චිත්‍රපටයකින් නොවේ for films

from elasticsearch import Elasticsearch
import json
import pandas
import math as m

elastic_client = Elasticsearch()
es_id = '160376l-ssb-data-2020-modified-index7'
# make an API call to the Elasticsearch cluster to get documents
result = elastic_client.search(index=es_id, body={}, size=1096)

all_documents = result['hits']['hits']

docs = pandas.DataFrame()
for num, doc in enumerate(all_documents):
    source_data = doc["_source"]
    _id = doc["_id"]
    doc_data = pandas.Series(source_data, name=_id)
    docs = docs.append(doc_data)

count1=0
count2=0
count3=0
for index, row in docs.iterrows():
    movie = row['movie']
    genre = row['genre']
    if (isinstance(movie, list) and isinstance(genre,list) ):
        if ( "චිත්‍රපටයකින් නොවේ" in movie and "චිත්‍රපට" in genre ):
                count1 += 1
                source_to_update = {
                    "doc": {
                        "movie": ["නොදන්‌නා"]
                    }
                }
                response = elastic_client.update(
                    index=es_id,
                    doc_type="_doc",
                    id=index,
                    body=source_to_update
                )
        elif  ("චිත්‍රපටයකින් නොවේ" in movie and not "චිත්‍රපට" in genre):
                count2 += 1
                source_to_update = {
                    "doc": {
                        "movie": ["නොවේ"]
                    }
                }
                response = elastic_client.update(
                    index=es_id,
                    doc_type="_doc",
                    id=index,
                    body=source_to_update
                )
    elif (isinstance(movie, str) and isinstance(genre,list) ):
        if (movie != "චිත්‍රපටයකින් නොවේ" and ( not "චිත්‍රපට" in genre and not "චිත්‍රපටය" in genre) ):
                print(movie)
                count3 += 1
                genre.append("චිත්‍රපට")
                source_to_update = {
                    "doc": {
                        "genre": genre
                    }
                }
                response = elastic_client.update(
                    index=es_id,
                    doc_type="_doc",
                    id=index,
                    body=source_to_update
                )
print(count1)
print(count2)
print(count3)
    
