from . import Matcher
from fuzzywuzzy import fuzz

class FuzzyMatcher(Matcher):

    def match(self, query, sort=False):
        """
        讀入使用者 query，若語料庫中存在相同的句子，便回傳該句子與標號
        """

        ratio  = -1
        target = ""
        target_idx = -1

        for index,title in enumerate(self.titles):

            newRatio = fuzz.ratio(query, title)
            if newRatio >= ratio:
                ratio  = newRatio
                target = title
                target_idx = index

        if sort:
            #TODO 斷詞後將句子重組，待確認有效性
            pass

        return index,target
