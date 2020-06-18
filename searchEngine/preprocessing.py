import io
from itertools import chain, combinations
from elasticsearch import Elasticsearch
from sinling import SinhalaTokenizer


class QueryProcessor:

    def __init__(self):
        self.tokenizer = SinhalaTokenizer()
        self.es = Elasticsearch()
        self.index = "160376l-ssb-data-2020-modified-index2"

    def advancedQuery(self, queryDictionary):

        multTermValue = []
        for i in queryDictionary:
            if (queryDictionary[i] != None and queryDictionary[i] != "") :
                tokens = self.tokenizer.tokenize(queryDictionary[i])
                stemmed_tokens = self.stemming(tokens)
                act = self.autocorrect(stemmed_tokens)
                flat_list_act = []
                for sublist in act:
                    for item in sublist:
                        flat_list_act.append(item)
                flat_list_act.append(queryDictionary[i])
                multTermValue.append({"terms": {i:flat_list_act, "boost":2}})
        print(multTermValue)
        res = self.es.search(
            index=self.index,
            body=
            {
                "query":
                    {
                        "bool": {
                            "should": multTermValue,
                        }
                    },
                    "size": 100,
                "aggs": {
                    "Artist Filter": {
                        "terms": {
                            "field": "artist.keyword",
                            "size": 10
                        }
                    },
                    "Composer Filter": {
                        "terms": {
                            "field": "composer.keyword",
                            "size": 10
                        }
                    },
                    "Genre Filter": {
                        "terms": {
                            "field": "genre.keyword",
                            "size": 10
                        }
                    },
                    "Movie Filter": {
                        "terms": {
                            "field": "movie.keyword",
                            "size": 10
                        }
                    },
                    "Writer Filter": {
                        "terms": {
                            "field": "writer.keyword",
                            "size": 10
                        }
                    },
                    "View Filter": {
                        "range": {
                            "field": "views",
                            "ranges": [
                                {
                                    "from": 0,
                                    "to": 1000
                                },
                                {
                                    "from": 1000,
                                    "to": 2000
                                },
                                {
                                    "from": 2000,
                                    "to": 3000
                                },
                                {
                                    "from": 3000
                                }
                            ]
                        }
                    }
                }
            }
        )
        results = res
        return results


    def generateMLTQuery(self, searchQuery, rankedlist):
        print("[INFO] Generating ranked Query")
        res = self.es.search(
            index=self.index,
            body=
            {
                "query":
                    {
                        "more_like_this": {
                            "fields": rankedlist,
                            "like": searchQuery,
                            "min_term_freq": 1,
                            "max_query_terms": 12
                        }
                    }
            }
        )
        results = res['hits']['hits']
        return results

    def generateTermsMultipleQuery(self,flat_list_act,fields, classDict):
        multTermValue = []
        sorted = False
        addedFields = []
        for i in fields:
            if(i != "popularity"):
                multTermValue.append({"terms": {i:flat_list_act, "boost":classDict[i]+1}})
                addedFields.append(i)
            else :
                sorted = True
                if(len(fields)==1):
                    for i in ["artist","writer","genre","composer"]:
                        multTermValue.append({"terms": {i: flat_list_act, "boost": 2}})
        for i in ["artist", "writer", "genre", "composer","movie"]:
            if i not in addedFields:
                multTermValue.append({"terms": {i: flat_list_act, "boost": 1 }})
        if(not sorted):
            for i in ["title","songLyricsSearchable"]:
                if i not in addedFields:
                    multTermValue.append({"terms": {i:flat_list_act}})
        if (not sorted):
            res = self.es.search(
                index=self.index,
                body=
                {
                    "query":
                        {
                            "bool": {
                                "should": multTermValue,
                            }
                        },
                "size": 100,
                "aggs": {
                    "Artist Filter": {
                        "terms": {
                            "field": "artist.keyword",
                            "size": 10
                        }
                    },
                    "Composer Filter": {
                        "terms": {
                            "field": "composer.keyword",
                            "size": 10
                        }
                    },
                    "Genre Filter": {
                        "terms": {
                            "field": "genre.keyword",
                            "size": 10
                        }
                    },
                    "Movie Filter": {
                        "terms": {
                            "field": "movie.keyword",
                            "size": 10
                        }
                    },
                    "Writer Filter": {
                        "terms": {
                            "field": "writer.keyword",
                            "size": 10
                        }
                    },
                    "View Filter": {
                        "range": {
                            "field": "views",
                            "ranges": [
                                {
                                    "from": 0,
                                    "to": 1000
                                },
                                {
                                    "from": 1000,
                                    "to": 2000
                                },
                                {
                                    "from": 2000,
                                    "to": 3000
                                },
                                {
                                    "from": 3000
                                }
                            ]
                        }
                    }
                }
                }
            )
        else :
            print("run query")
            res = self.es.search(
                index=self.index,
                body=
                {
                    "query":
                        {
                            "bool": {
                                "should": multTermValue
                            }
                        },
                    "sort": [
                        "_score",
                        {"views":  { "order": "desc" }}
                    ],
                "size": 100,
                "aggs": {
                    "Artist Filter": {
                        "terms": {
                            "field": "artist.keyword",
                            "size": 10
                        }
                    },
                    "Composer Filter": {
                        "terms": {
                            "field": "composer.keyword",
                            "size": 10
                        }
                    },
                    "Genre Filter": {
                        "terms": {
                            "field": "genre.keyword",
                            "size": 10
                        }
                    },
                    "Movie Filter": {
                        "terms": {
                            "field": "movie.keyword",
                            "size": 10
                        }
                    },
                    "Writer Filter": {
                        "terms": {
                            "field": "writer.keyword",
                            "size": 10
                        }
                    },
                    "View Filter": {
                        "range": {
                            "field": "views",
                            "ranges": [
                                {
                                    "from": 0,
                                    "to": 1000
                                },
                                {
                                    "from": 1000,
                                    "to": 2000
                                },
                                {
                                    "from": 2000,
                                    "to": 3000
                                },
                                {
                                    "from": 3000
                                }
                            ]
                        }
                    }
                }
                }
            )
        results = res
        return results

    def generateTermsSingleQuery(self,flat_list_act,field):
        res = self.es.search(
            index=self.index,
            body=
            {
                "query":
                    {
                        "terms": {
                            field: flat_list_act
                        }
                    }
            }
        )
        results = res['hits']['hits']
        return results

    def generateNormalQuery(self, flat_list_act):
        print("[INFO] Generating Normal Query")
        multTermValue = []
        for i in ["artist","writer","genre","composer","title","songLyricsSearchable","movie"]:
            multTermValue.append({"terms": {i: flat_list_act,"boost":1}})
        print(multTermValue)
        res = self.es.search(
            index=self.index,
            body=
            {
                "query":
                    {
                        "bool": {
                            "should": multTermValue
                        }
                    },
                "size": 100,
                "aggs": {
                    "Artist Filter": {
                        "terms": {
                            "field": "artist.keyword",
                            "size": 10
                        }
                    },
                    "Composer Filter": {
                        "terms": {
                            "field": "composer.keyword",
                            "size": 10
                        }
                    },
                    "Genre Filter": {
                        "terms": {
                            "field": "genre.keyword",
                            "size": 10
                        }
                    },
                    "Movie Filter": {
                        "terms": {
                            "field": "movie.keyword",
                            "size": 10
                        }
                    },
                    "Writer Filter": {
                        "terms": {
                            "field": "writer.keyword",
                            "size": 10
                        }
                    },
                    "View Filter": {
                        "range": {
                            "field": "views",
                            "ranges": [
                                {
                                    "from": 0,
                                    "to": 1000
                                },
                                {
                                    "from": 1000,
                                    "to": 2000
                                },
                                {
                                    "from": 2000,
                                    "to": 3000
                                },
                                {
                                    "from": 3000
                                }
                            ]
                        }
                    }
                }
            }
        )
        results = res
        return results

    def generateQuery(self, searchQuery):
        print("[INFO] Generating Query")
        tokens = self.tokenizer.tokenize(searchQuery)
        stemmed_tokens = self.stemming(tokens)
        act = self.autocorrect(stemmed_tokens)
        flat_list_act = []
        for sublist in act:
            for item in sublist:
                flat_list_act.append(item)
        classDict = self.searchClassification(act)
        if (len(classDict) <= 0):
            results = self.generateNormalQuery(flat_list_act)
            # self.generateMLTQuery(searchQuery, ["artist","songLyricsSearchable","writer","composer","genre"])
        else:
            rankedlist = []
            for i in classDict:
                if (i in ["writer", "composer", "artist", "genre", "popularity"]):
                    rankedlist.append(i)
            if ( len(rankedlist) > 0):
                results = self.generateTermsMultipleQuery(flat_list_act, rankedlist, classDict)
            #self.generateFuzzyQuery()
        return results

    def getSubsets(self, iterable):
        return chain.from_iterable(combinations(iterable, r) for r in range(len(iterable) + 1))

    # Observe tokens and return query type as 'Normal Lyric Search', 'Feature Search', 'Ranked Feature Search'
    def searchClassification(self, tokens):

        synonyms = "synonyms.txt"
        try:
            synonymsFile = io.open(synonyms, "r", encoding='utf-8').read()
        except UnicodeDecodeError:
            synonymsFile = io.open(synonyms, "r", encoding='latin-1').read()
        synonymsList = synonymsFile.split("\n")
        synonymsDict = {}
        for i in synonymsList:
            splitSynonymLine = i.split(":")
            try:
                synonymsDict[splitSynonymLine[0]] = splitSynonymLine[1].split(",")
            except:
                print()
        rankedQuery = {}
        for corrected_tokens in tokens:
            for token in corrected_tokens:
                foundsynonym = False
                for key in synonymsDict:
                    if token in synonymsDict[key]:
                        if rankedQuery.get(key) == None:
                            rankedQuery[key] = 1
                        else:
                            rankedQuery[key] = rankedQuery[key] + 1
                        foundsynonym = True
                if foundsynonym:
                    break
        return rankedQuery

    # Looks at basic error rules within the Sinhala Lanugage and appends likely errors
    def autocorrect(self, tokens):
        allWords = [[] for i in range(len(tokens))]
        missFileDirec = "mispellings.txt"
        try:
            misspellingsFile = io.open(missFileDirec, "r", encoding='utf-8').read()
        except UnicodeDecodeError:
            misspellingsFile = io.open(missFileDirec, "r", encoding='latin-1').read()
        missList = misspellingsFile.split()
        missListSet = []
        for i in missList:
            missListSet.append(i.split(','))
        for token_number in range(len(tokens)):
            token = tokens[token_number]
            missListForWord = []
            for misspellPairs in missListSet:
                if misspellPairs[0] in token or misspellPairs[1] in token:
                    missListForWord.append(misspellPairs)
            for j in list(self.getSubsets(missListForWord)):
                for d in list(j):
                    if d[0] in token:
                        token = token.replace(d[0], d[1])
                    elif d[1] in token:
                        token = token.replace(d[1], d[0])
                allWords[token_number].append(token)
        return allWords

    def rreplace(self,s, old, new, occurrence):
        li = s.rsplit(old, occurrence)
        return new.join(li)


    # Reduce strings to simple formats based on rules
    def stemming(self, doc):
        suffFileDirec = "suffixes.txt"
        try:
            suffixFile = io.open(suffFileDirec, "r", encoding='utf-8').read()
        except UnicodeDecodeError:
            suffixFile = io.open(suffFileDirec, "r", encoding='latin-1').read()

        suffixList = suffixFile.split()

        doc.sort()
        stemmedWordlist = []
        stemmedWordlist.extend(doc)

        for i in doc:
            for j in suffixList:
                if i.endswith(j):
                    stemmedWordlist.append(self.rreplace(i,j, "",1))
        print(stemmedWordlist)
        return stemmedWordlist

#qp = QueryProcessor()
#qp.generateQuery("හොඳම අමරදේව")
