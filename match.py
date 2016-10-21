import json
import os
import random

from Matcher.fuzzyMatcher import FuzzyMatcher
from Matcher.wordWeightMatcher import WordWeightMatcher
from Matcher.matcher import Matcher

def main():
    matcherTesting("Fuzzy", threshold=0.5)
    #fuzzyMatch(threshold=50)
    #woreWeightMatch(threshold=0.5)


def getMatcher(matcherType):

    if matcherType == "WordWeight":
        return woreWeightMatch()
    elif matcherType == "Fuzzy":
        return fuzzyMatch()
    elif matcherType == "Vectorize":
        pass #TODO
    elif matcherType == "DeepLearning":
        pass #TODO
    else:
        print("[Error]: Invailded type.")
        exit()

def matcherTesting(matcherType, threshold=0.5):

    matcher = getMatcher(matcherType)
    while True:
        query = input("隨便說些什麼吧: ")
        title,index = matcher.match(query,threshold)
        sim = matcher.getSimilarity()
        print("最為相似的標題是 %s ，相似度為 %d " % (title,sim))

        res = json.load(open(os.path.join("data/processed/reply/",str(int(index/1000))+'.json'),'r',encoding='utf-8'))
        targetId = index % 1000
        #randomId = random.randrange(0,len(res[targetId]))

        for content in res[targetId]:
            print(content["Content"])


def woreWeightMatch():

    weightMatcher = WordWeightMatcher(segLib="Taiba")
    weightMatcher.loadTitles(path="data/Titles.txt")
    weightMatcher.initialize()
    return weightMatcher

def fuzzyMatch():
    fuzzyMatcher = FuzzyMatcher(segLib="Taiba")
    fuzzyMatcher.loadTitles(path="data/Titles.txt")
    return fuzzyMatcher

    #load a custom user dictionary.
    #fuzzyMatcher.TaibaCustomSetting(usr_dict="jieba_dictionary/ptt_dic.txt")

    #load stopwords
    #fuzzyMatcher.loadStopWords(path="data/stopwords/chinese_sw.txt")
    #fuzzyMatcher.loadStopWords(path="data/stopwords/ptt_words.txt")
    #fuzzyMatcher.loadStopWords(path="data/stopwords/specialMarks.txt")


if __name__ == '__main__':
    main()
