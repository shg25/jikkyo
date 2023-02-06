import os
import re

from janome.analyzer import Analyzer
from janome.charfilter import UnicodeNormalizeCharFilter, RegexReplaceCharFilter
from janome.tokenfilter import CompoundNounFilter, LowerCaseFilter, POSKeepFilter
from janome.tokenizer import Tokenizer

import config
import constant
from functions import remove_emoji

outputPath = config.OUTPUT_PATH

if not os.path.isdir(outputPath):
    os.mkdir(outputPath)

wordsFile = open(outputPath + '/' + constant.WORDS_FILE_PATH, 'w')
tweetsTxtFile = open(outputPath + '/' + constant.TWEETS_TXT_FILE_PATH, 'r')
txt = tweetsTxtFile.read()

# 形態素解析オブジェクトの生成
# t = Tokenizer('dic.csv', mmap=True)
charFilters = [
    UnicodeNormalizeCharFilter(),
    RegexReplaceCharFilter(u'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+', ''),
    RegexReplaceCharFilter(u'ーー', 'ー')
]
# t = Tokenizer(mmap=True)
t = Tokenizer()
tokenFilters = [
    CompoundNounFilter(),
    POSKeepFilter(['名詞']),
    LowerCaseFilter()
]
# analyzer = Analyzer(charFilters, t, tokenFilters)
analyzer = Analyzer(char_filters=charFilters, tokenizer=t, token_filters=tokenFilters)

# テキストを一行ずつ処理
wordDic = {}
lines = txt.split("\r\n")
for line in lines:
    analyzedList = analyzer.analyze(line)
    for w in analyzedList:
        word = w.surface
        if remove_emoji(word) == "":
            continue
        if re.match('^[w]+$', word):
            continue  # 「w」だけが1つ以上連続
        if re.match('^[ー]+$', word):
            continue  # 「ー」だけが1つ以上連続
        if re.match('^[笑]+$', word):
            continue  # 「笑」だけが1つ以上連続
        if re.match('^[0-9\-]+$', word):
            continue  # 数字とハイフンだけが1つ以上連続
        if len(word) == 1 and re.match('[a-zA-ZΑ-ωА-я─-╂ぁ-ん艸゚]', word):
            continue  # ひらがな1文字だけ

        # 「w」を除外した結果、英語が残っていなかったら、「w」を除外したものを採用
        wSub = re.sub(r'[w]+', "", word)
        if re.match(r'[^a-zA-Z]+', wSub):
            word = wSub

        # if re.match('([w])\1{1,}', word):
        #     continue
        if not word in wordDic:
            wordDic[word] = 0
        wordDic[word] += 1  # カウント

# よく使われる単語を表示
keys = sorted(wordDic.items(), key=lambda x: x[1], reverse=True)
for word, cnt in keys[:400]:
    outputText = "{0};{1}\n".format(word, cnt)
    # print(outputText)
    wordsFile.write(outputText)

wordsFile.close()
tweetsTxtFile.close()
