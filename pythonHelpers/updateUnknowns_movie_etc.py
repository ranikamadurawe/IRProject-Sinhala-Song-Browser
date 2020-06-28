# This script is used to change any songs with no movies and or unknown keys and bests from the incosistent format to a consistent format of an index
# The chosen format was to apply "නොදන්‌නා" for keys and beats and චිත්‍රපටයකින් නොවේ for films

from elasticsearch import Elasticsearch
import json
import pandas
import math as m

elastic_client = Elasticsearch()
es_id = '160376l-ssb-data-2020-modified-index4'
# make an API call to the Elasticsearch cluster to get documents
result = elastic_client.search(index=es_id, body={}, size=1096)

all_documents = result['hits']['hits']

docs = pandas.DataFrame()
for num, doc in enumerate(all_documents):
    source_data = doc["_source"]
    _id = doc["_id"]
    doc_data = pandas.Series(source_data, name=_id)
    docs = docs.append(doc_data)

for index, row in docs.iterrows():
    movie = row['movie']
    key = row['key']
    beat = row['beat']
    if (not isinstance(movie, str) and not isinstance(movie,list)):
        if (m.isnan(movie)):
                source_to_update = {
                    "doc": {
                        "movie": ["චිත්‍රපටයකින් නොවේ"]
                    }
                }
                response = elastic_client.update(
                    index=es_id,
                    doc_type="_doc",
                    id=index,
                    body=source_to_update
                )
    if (not isinstance(key, str) and not isinstance(key,list)):
        if (m.isnan(key)):
                source_to_update = {
                    "doc": {
                        "key": ["නොදන්‌නා"]
                    }
                }
                response = elastic_client.update(
                    index=es_id,
                    doc_type="_doc",
                    id=index,
                    body=source_to_update
                )
    if (not isinstance(beat, str) and not isinstance(beat,list)):
        if (m.isnan(beat)):
                source_to_update = {
                    "doc": {
                        "beat": ["නොදන්‌නා"]
                    }  
                }
                response = elastic_client.update(
                    index=es_id,
                    doc_type="_doc",
                    id=index,
                    body=source_to_update
                ) 
