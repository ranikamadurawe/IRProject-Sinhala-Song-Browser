# This script is used to change any songs with unknown artists, writers or composers from the incosistent format of either "නොදත්‌", "නොදන්‌නා" and null to consistent format
# The chosen format was to apply ["නොදන්‌නා"]

from elasticsearch import Elasticsearch
import json
import pandas
import math as m

elastic_client = Elasticsearch()
es_id = '160376l-ssb-data-2020-modified-index2'
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
    artist = row['artist']
    writer = row['writer']
    composer = row['composer']
    genre = row['genre']
    if (not isinstance(artist, list)):
        if (artist[0] == "නොදත්‌" and len(artist) == 1):
            source_to_update = {
                "doc": {
                    "artist": ["නොදන්‌නා"]
                }
            }
            response = elastic_client.update(
                index=es_id,
                doc_type="_doc",
                id=index,
                body=source_to_update
            )
    if (not isinstance(writer, list)):
        if (writer[0] == "නොදත්‌" and len(writer) == 1):
            source_to_update = {
                "doc": {
                    "writer": ["නොදන්‌නා"]
                }
            }
            response = elastic_client.update(
                index=es_id,
                doc_type="_doc",
                id=index,
                body=source_to_update
            )

    if (not isinstance(composer, list)):
        if (composer[0] == "නොදත්‌" and len(composer) == 1):
            source_to_update = {
                "doc": {
                    "composer": ["නොදන්‌නා"]
                }
            }
            response = elastic_client.update(
                index=es_id,
                doc_type="_doc",
                id=index,
                body=source_to_update
            )
    if (not isinstance(genre, list)):
        if (genre[0] == "නොදත්‌" and len(genre) == 1):
            source_to_update = {
                "doc": {
                    "genre": ["නොදන්‌නා"]
                }
            }
            response = elastic_client.update(
                index=es_id,
                doc_type="_doc",
                id=index,
                body=source_to_update
            )
