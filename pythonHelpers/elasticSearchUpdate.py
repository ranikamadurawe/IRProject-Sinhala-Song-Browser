from elasticsearch import Elasticsearch
import json
import pandas

elastic_client = Elasticsearch()

# make an API call to the Elasticsearch cluster to get documents
result = elastic_client.search(index='160376l-ssb-data-2020_backup', body={}, size=1096)

all_documents = result['hits']['hits']


docs = pandas.DataFrame()
for num, doc in enumerate(all_documents):
    source_data = doc["_source"]
    _id = doc["_id"]
    doc_data = pandas.Series(source_data, name=_id)
    docs = docs.append(doc_data)

for index, row in docs.iterrows():
    newlinesplit = row['songLyrics'].split("\n")
    newsplitremovewhitespace = []
    for i in newlinesplit:
        x = " ".join(i.split())
        if (x != ''):
            newsplitremovewhitespace.append(x)
    newSongLyric = "\n".join(newsplitremovewhitespace)
    newSongSearch = " ".join(row['songLyricsSearchable'].split())
    source_to_update = {
        "doc": {
            "songLyricsSearchable": newSongSearch,
            'songLyrics': newSongLyric
        }
    }
    response = elastic_client.update(
        index='160376l-ssb-data-2020_backup',
        doc_type="_doc",
        id = index,
        body = source_to_update
    )









