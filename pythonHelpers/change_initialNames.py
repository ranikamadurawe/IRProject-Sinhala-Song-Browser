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

all_namesSet = set()
change_dict = {
  'එච්.ආර්.ජෝතිපාල' : 'එච්.ආර්. ජෝතිපාල', 
  'පී.එල්.ජේ.නන්දකීර්ති' : 'පී.එල්.ජේ. නන්දකීර්ති' , 
  'ජේ.ඒ.දොඩංගොඩ' : 'ජේ.ඒ. දොඩංගොඩ', 
  'ආර්.මුත්තුසාමි' : 'ආර්. මුත්තුසාමි', 
  'ඩබ්ලිව්.ඩී.අරියසිංහ' : 'ඩබ්ලිව්.ඩී. අරියසිංහ', 
  'ඒ.එම්.රාජා' : 'ඒ.එම්. රාජා', 
  'ඩබ්.ඩී.අමරදේව' : 'ඩබ්.ඩී. අමරදේව', 
  'එච්.ආර්.චන්ද්\u200dරසේන' : 'එච්.ආර්. චන්ද්\u200dරසේන', 
  'එච්.ආර්.ජෝතිපාල ': 'එච්.ආර්. ජෝතිපාල', 
  'ආර්.බී.ජයාසිංහ' : 'ආර්.බී. ජයාසිංහ', 
  'එම්.එස්.ප්\u200dරනාන්දු ' : 'එම්.එස්. ප්\u200dරනාන්දු', 
  'ආර්.ප්\u200dරෙමදාස' : 'ආර්. ප්\u200dරෙමදාස', 
  'සී.ටී.ෆර්නාන්ඩෝ' : 'සී.ටී. ෆර්නාන්ඩෝ', 
  ' සී.ටී.ප්\u200dරනාන්දු' : 'සී.ටී. ප්\u200dරනාන්දු', 
  'B.S.Perera' : 'බි.එස්‌. පෙරේරා', 
  'ඒ.ජේ.කරීම්' : 'ඒ.ජේ. කරීම්', 
  'එච්.ආර්.ජෝතිපාල H.R.Jothipala' : "එච්.ආර්. ජෝතිපාල", 
  'ටී.වී.කුසුම්පාල' : 'ටී.වී. කුසුම්පාල', 
  'පී.එල්.ඒ.සෝමපාල' : 'පී.එල්.ඒ. සෝමපාල', 
  'පී.එස්.අලවත්තගේ' : 'පී.එස්. අලවත්තගේ', 
  ' එච්.ආර්.ජෝතිපාල' : "එච්.ආර්. ජෝතිපාල" , 
  'එම්.ආර්.කුලසිංහ' : 'එම්.ආර්. කුලසිංහ', 
  'ගලගෙදර එම්.එම්.ඒ.හුක්' : 'ගලගෙදර එම්.එම්.ඒ. හුක්', 
  'එම්.කේ.රොක්සාමි' : 'එම්.කේ. රොක්සාමි', 
  'ටී.ආර්.පාපා' : 'ටී.ආර්. පාපා', 
  'ආර්.ඒ.චන්ද්\u200dරසේන' : 'ආර්.ඒ. චන්ද්\u200dරසේන',  
  'ටී.එම්.ජයරත්න': 'ටී.එම්. ජයරත්න', 
  'සී.ටී.පෙරෙරා' : 'සී.ටී. පෙරෙරා', 
  'එච්.ආර්ඤජෝතිපාල' : 'එච්. ආර්ඤජෝතිපාල', 
  'ඩී.ආර්.පියරිස්' : 'ඩී.ආර්. පියරිස්', 
  'එම්.එස්.ප්\u200dරනාන්දු' : 'එම්.එස්. ප්\u200dරනාන්දු', 
  'K.A.W.Perera' : "කේ.ඒ.ඩබ්‌ලිව්‌. පෙරේරා", 
  'එච්.එම්.ජයරත්න': 'එච්.එම්. ජයරත්න'}

for index, row in docs.iterrows():
    artist = row['artist']
    writer = row['writer']
    composer = row['composer']
    art_changed = False
    writ_changed = False
    comp_changed = False
    for i in range(len(artist)) : 
         if ( artist[i] in  change_dict) :
             old_val = artist[i]
             artist[i] = change_dict[old_val]
             art_changed = True
             print(artist)
    for i in range(len(writer)) : 
         if ( writer[i] in  change_dict ) :
             old_val = writer[i]
             writer[i] = change_dict[old_val]
             writ_changed = True    
             print(writer)
    for i in range(len(composer)) :  
         if ( composer[i] in  change_dict) :
             old_val = composer[i]
             composer[i] = change_dict[old_val]
             comp_changed = True
             print(composer)
    if art_changed :
         source_to_update = {
                "doc": {
                    "artist": artist
                }
            }
         response = elastic_client.update(
                index=es_id,
                doc_type="_doc",
                id=index,
                body=source_to_update
            )
    if writ_changed :
         source_to_update = {
                "doc": {
                    "writer": writer
                }
            }
         response = elastic_client.update(
                index=es_id,
                doc_type="_doc",
                id=index,
                body=source_to_update
            )  
    if comp_changed :
         source_to_update = {
                "doc": {
                    "composer": composer
                }
            }
         response = elastic_client.update(
                index=es_id,
                doc_type="_doc",
                id=index,
                body=source_to_update
            )

