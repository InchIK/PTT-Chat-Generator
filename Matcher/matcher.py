import logging

import jieba
import Taiba

class Matcher(object):

    """
    比對使用者輸入的句子與目標語料集，
    回傳語料集中最相似的一個句子。
    """

    def __init__(self, segLib="Taiba"):

        logging.basicConfig(format='%(asctime)s : %(threadName)s : %(levelname)s : %(message)s', level=logging.INFO)
        self.titles = [] # 欲進行匹配的所有標題
        self.segTitles = [] # 斷好詞的標題

        self.stopwords = set()
        self.similarity = 1.

        if segLib == "Taiba":
            self.useTaiba = True
        else:
            self.useTaiba = False

    def jiebaCustomSetting(self, dict_path, usr_dict_path):

        jieba.set_dictionary(dict_path)
        with open(usr_dict_path, 'r', encoding='utf-8') as dic:
            for word in dic:
                jieba.add_word(word.strip('\n'))

    def TaibaCustomSetting(self, usr_dict):

        with open(usr_dict, 'r', encoding='utf-8') as dic:
            for word in dic:
                Taiba.add_word(word.strip('\n'))

    def loadStopWords(self, path):
        with open(path, 'r', encoding='utf-8') as sw:
            for word in sw:
                self.stopwords.add(word.strip('\n'))

    def loadTitles(self, path):

        with open(path,'r',encoding='utf-8') as data:
            self.titles = [line.strip('\n') for line in data]

    def match(self, query):
        """
        讀入使用者 query，若語料庫中存在相同的句子，便回傳該句子與標號
        """
        result = None
        for index, title in enumerate(self.titles):
            if title == query:
                return title,index

    def getSimilarity(self):
        return self.similarity

    def wordSegmentation(self, string):

        if self.useTaiba:
            return Taiba.lcut(string,CRF=True)
        else:
            return jieba.cut(string,cut_all=True)

    def TitlesSegmentation(self):

        """
        將 self.titles 斷詞後的結果輸出，並儲存於 self.segTitles
        """

        logging.info("正準備將 titles 斷詞")

        count = 0

        self.segTitles = []
        for title in self.titles:
            self.segTitles.append(self.wordSegmentation(title))

            count += 1
            if count % 1000 == 0:
                logging.info("已斷詞完前 %d 篇文章" % count)

        with open('data/SegTitles.txt','w',encoding="utf-8") as seg_title:
            for title in self.segTitles:
                seg_title.write(' '.join(title) + '\n')
        logging.info("完成標題斷詞，結果已暫存至 data/SegTitles.txt")
