import io
from itertools import chain, combinations
from elasticsearch import Elasticsearch
from sinling import SinhalaTokenizer


class QueryProcessor:

    def __init__(self):
        self.tokenizer = SinhalaTokenizer()
        self.es = Elasticsearch()
        self.index = "160376l-ssb-data-2020-modified-index"

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
        for i in results:
            print(i)

    def generateTermsMultipleQuery(self,flat_list_act,fields, classDict):
        multTermValue = []
        sorted = False
        for i in fields:
            if(i != "popularity"):
                multTermValue.append({"terms": {i:flat_list_act, "boost":classDict[i]+1}})
            else :
                sorted = True
                if(len(fields)==1):
                    for i in ["artist", "writer", "genre", "composer"]:
                        multTermValue.append({"terms": {i: flat_list_act, "boost": 2}})
        multTermValue.append({"terms": {"songLyricsSearchable":flat_list_act}})
        multTermValue.append({"terms": {"title": flat_list_act}})
        print(multTermValue)
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
                        }
                }
            )
        else :
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
                        {"views": "desc"}
                    ]
                }
            )
        results = res['hits']['hits']
        for i in results:
            print(i)

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
        for i in results:
            print(i)

    def generateNormalQuery(self, flat_list_act):
        print("[INFO] Generating Normal Query")
        multTermValue = []
        for i in ["artist","writer","genre","composer","title","songLyricsSearchable"]:
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
                    }
            }
        )
        results = res['hits']['hits']
        for i in results:
            print(i)

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
            self.generateNormalQuery(flat_list_act)
            # self.generateMLTQuery(searchQuery, ["artist","songLyricsSearchable","writer","composer","genre"])
        else:
            rankedlist = []
            for i in classDict:
                if (i in ["writer", "composer", "artist", "genre", "popularity"]):
                    rankedlist.append(i)
            if ( len(rankedlist) > 0):
                self.generateTermsMultipleQuery(flat_list_act, rankedlist, classDict)
            #self.generateFuzzyQuery()

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
                        break
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
                    i = i.replace(j, "")
                    break
            stemmedWordlist.append(i)

        return stemmedWordlist

qp = QueryProcessor()
qp.generateQuery("හොඳම අමරදේව")