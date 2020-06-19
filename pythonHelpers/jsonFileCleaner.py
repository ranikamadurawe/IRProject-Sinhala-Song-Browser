from elasticsearch import Elasticsearch
import json
import pandas

elastic_client = Elasticsearch()

# make an API call to the Elasticsearch cluster to get documents
result = elastic_client.search(index='160376l-ssb-data-2020', body={}, size=1096)

elastic_docs = result['hits']['hits']

docs = pandas.DataFrame()

for num, doc in enumerate(elastic_docs):
    # get _source data dict from document
    source_data = doc["_source"]

    # get _id from document
    _id = doc["_id"]
    doc_data = pandas.Series(source_data, name=_id)

    # append the Series object to the DataFrame object
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
    docs.at[index, 'songLyricsSearchable'] = newSongSearch
    docs.at[index, 'songLyrics'] = newSongLyric

docs.to_json("songs.json", "records")
