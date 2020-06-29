import io
from itertools import chain, combinations
from elasticsearch import Elasticsearch
from sinling import SinhalaTokenizer
from mtranslate import translate
import re


class QueryProcessor:

    def __init__(self):
        self.tokenizer = SinhalaTokenizer()
        self.es = Elasticsearch()
        self.index = "160376l-ssb-data-2020-modified-index7"
        self.translation_dict = {}

    # Translate a word from English to Sinhala
    def translate_word(self, word):
        translated = translate(word, 'si', 'en')
        return translated

    # Translate an array from English to Sinhala
    def translate_array(self, wordlist):
        isAscii = lambda s: len(s) == len(s.encode())
        translated_array = []
        for i in wordlist:
            # Check if word is made of ASCII Letters
            if isAscii(i):
                if i in self.translation_dict.keys():
                    translated_array.append(self.translation_dict.get(i))
                else:
                    translated_phrase = self.translate_word(i)
                    self.translation_dict[i] = translated_phrase
                    translated_array.append(translated_phrase)
        return translated_array

    # Genereate ES Query for Advacned Queries
    def advancedQuery(self, queryDictionary):
        multTermValue = []
        for i in queryDictionary:
            if (queryDictionary[i] != None and queryDictionary[i] != ""):
                queryDictionary[i] = queryDictionary[i].replace("."," ")
                tokens = self.tokenizer.tokenize(queryDictionary[i])
                tokens.extend(self.translate_array(tokens))
                stemmed_tokens = self.stemming(tokens)
                act = self.autocorrect(stemmed_tokens)
                flat_list_act = []
                for sublist in act:
                    for item in sublist:
                        flat_list_act.append(item)
                flat_list_act.append(queryDictionary[i])
                multTermValue.append({"terms": {i: flat_list_act, "boost": 2}})
        # Generate a ES Boolean Query
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
                    "Key Filter": {
                        "terms": {
                            "field": "key.keyword",
                            "size": 10
                        }
                    },
                    "Beat Filter": {
                        "terms": {
                            "field": "beat.keyword",
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

    # Generate ES Query with Boosted MetaData tags
    def generateTermsMultipleQuery(self, flat_list_act, fields, classDict, searchQuery):
        multTermValue = []
        sorted = False
        addedFields = []
        for i in fields:
            if (i != "popularity"):
                multTermValue.append({"terms": {i: flat_list_act, "boost": classDict[i] + 1}})
                addedFields.append(i)
            else:
                sorted = True
                if (len(fields) == 1):
                    for i in ["writer", "composer", "artist", "genre", "key", "beat", "movie"]:
                        multTermValue.append({"terms": {i: flat_list_act, "boost": 2}})
        for i in ["writer", "composer", "artist", "genre", "key", "beat", "movie"]:
            if i not in addedFields:
                multTermValue.append({"terms": {i: flat_list_act, "boost": 1}})
        if (not sorted):
            for i in ["title", "songLyricsSearchable"]:
                if i not in addedFields:
                    multTermValue.append({"terms": {i: flat_list_act}})
                    multTermValue.append({"match_phrase": {i: searchQuery}})
        # If no ranking terms (i.e හොඳම) have been provided do not sort results
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
                        "Key Filter": {
                            "terms": {
                                "field": "key.keyword",
                                "size": 10
                            }
                        },
                        "Beat Filter": {
                            "terms": {
                                "field": "beat.keyword",
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
        # If ranking terms (i.e හොඳම) have been provided sort results based on the function score
        else:
            print("run query")
            res = self.es.search(
                index=self.index,
                body=
                {
                    "query": {
                        "function_score": {
                            "functions": [
                                {
                                    "field_value_factor": {
                                        "field": "views",
                                        "factor": 1.0001,
                                        "missing": 1
                                    }
                                }
                            ],
                            "query":
                                {
                                    "bool": {
                                        "should": multTermValue
                                    }
                                },
                            # "sort": [
                            #     "_score",
                            #     {"views":  { "order": "desc" }}
                            # ],

                            "score_mode": "multiply"
                        },

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
                        "Key Filter": {
                            "terms": {
                                "field": "key.keyword",
                                "size": 10
                            }
                        },
                        "Beat Filter": {
                            "terms": {
                                "field": "beat.keyword",
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

    # Generate a Normal Query with no Boosted MetaData tags
    def generateNormalQuery(self, flat_list_act, searchQuery):
        print("[INFO] Generating Normal Query")
        multTermValue = []
        for i in ["artist", "writer", "genre", "composer", "title", "songLyricsSearchable", "movie", "beat", "key"]:
            multTermValue.append({"terms": {i: flat_list_act, "boost": 1}})
            multTermValue.append({"match_phrase": {i: searchQuery}})
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
                    "Key Filter": {
                        "terms": {
                            "field": "key.keyword",
                            "size": 10
                        }
                    },
                    "Beat Filter": {
                        "terms": {
                            "field": "beat.keyword",
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

    # Analyze the word and generate appropriate keyword for user's search request
    def generateQuery(self, searchQuery):
        print("[INFO] Generating Query")
        searchQuery = searchQuery.replace("."," ")
        tokens = self.tokenizer.tokenize(searchQuery)
        tokens.extend(self.translate_array(tokens))
        stemmed_tokens = self.stemming(tokens)
        act = self.autocorrect(stemmed_tokens)
        flat_list_act = []
        for sublist in act:
            for item in sublist:
                flat_list_act.append(item)
        classDict = self.searchClassification(act)
        if (len(classDict) <= 0):
            results = self.generateNormalQuery(flat_list_act, searchQuery)
            # self.generateMLTQuery(searchQuery, ["artist","songLyricsSearchable","writer","composer","genre"])
        else:
            rankedlist = []
            for i in classDict:
                if (i in ["writer", "composer", "artist", "genre", "popularity", "key", "beat", "movie"]):
                    rankedlist.append(i)
                    if i == "key":
                        p = re.compile(r"[A-G,a-g][b,#]{0,1} (major|minor|Major|Major)")
                        r = p.search(searchQuery)
                        flat_list_act.append(r[0])
                    if i == "beat":
                        p = re.compile(r"\b[0-9]{1,2}\/[0-9]{1,2}")
                        r = p.findall(searchQuery)
                        flat_list_act.append(r[0])
            if (len(rankedlist) > 0):
                results = self.generateTermsMultipleQuery(flat_list_act, rankedlist, classDict, searchQuery)
            # self.generateFuzzyQuery()
        return results

    def getSubsets(self, iterable):
        return chain.from_iterable(combinations(iterable, r) for r in range(len(iterable) + 1))

    # Observe tokens and return query type
    # If special keyword boosting terms exist return the presence of those keywords
    def searchClassification(self, tokens):

        synonyms = "resource_files/synonyms.txt"
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
        missFileDirec = "resource_files/mispellings.txt"
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
            print(list(self.getSubsets(missListForWord)))
            for j in list(self.getSubsets(missListForWord)):
                k = token
                for d in list(j):
                    if d[0] in k:
                        k = k.replace(d[0], d[1])
                    elif d[1] in token:
                        k = k.replace(d[1], d[0])
                allWords[token_number].append(k)
        return allWords

    def rreplace(self, s, old, new, occurrence):
        li = s.rsplit(old, occurrence)
        return new.join(li)

    # Reduce strings to simple formats based on rules
    def stemming(self, doc):
        suffFileDirec = "resource_files/suffixes.txt"
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
                    stemmedWordlist.append(self.rreplace(i, j, "", 1))
        return stemmedWordlist
