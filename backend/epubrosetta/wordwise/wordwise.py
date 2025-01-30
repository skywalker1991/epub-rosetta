# -*- coding: utf-8 -*-
"""
file
"""
import re

# 定义wordwise处理类
class Wordwise:
    def __init__(self,dict,lemma,html,style):
        self.dict = dict
        self.lemma = lemma
        self.html = html
        self.style = style

    # 分离 HTML 标签和文字部分
    def __split_html(self):
        segments = re.split(r"(<[^>]+>)", self.html)
        return segments
    
    # 查询单词原型
    def __query_lemma(self,word):
        '''
        word: str
        '''
        return self.lemma.word_stem(word)
    
    # 查询单词释义
    def __query_word(self,word):
        '''
        word: str
        settings: dict
        '''
        # 去除单词前后的标点符号
        word = word.strip(".,!?()[]{}")
        # 将单词转换为小写
        word = word.lower()

        # 查询该词的原型，如果存在
        lemma = self.__query_lemma(word)

        if lemma:
            query_result = self.dict.query(lemma)
            wordlen = len(lemma)
            return self.__process_query_result(query_result,wordlen)
        query_result = self.dict.query(word)
        wordlen = len(word)
        return self.__process_query_result(query_result,wordlen)

    # 对查询结果进行精简处理,保留第一个换行符之前的内容
    def __process_query_result(self,query_result,wordlen):
        '''
        query_result: str
        '''
        if query_result:
            # 获取translation字段的内容
            query_result = query_result.get("translation", "")
            # 返回释义的字符串中对&，<，>进行转义
            query_result = query_result.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            # 取第一个换行符之前的内容，且是分号前的内容
            query_result = query_result.split("\n")[0]
            # 根据单词长度，对释义进行截取
            query_result = query_result[:wordlen*2]
            # 如果返回结果有逗号，去除最后一个逗号以后的内容
            if "," in query_result:
                query_result = query_result[:query_result.rfind(",")]
            
            if query_result:
                return query_result
        else:
            return ""

    
    # 标注指定的单词
    def by_word(self,words):
        '''
        words: list
        '''
        segments = self.__split_html()
        processed_segments = []
        for segment in segments:
            if segment.startswith("<"):
                processed_segments.append(segment)
            else:
                paragraph_words = re.split(r"(\s+)", segment)
                processed_words = []
                for word in paragraph_words:
                    if word.strip():
                        if word in words:
                            word_meaning = self.__query_word(word)
                            if word_meaning:
                                processed_words.append(f"<ruby>{word}<rt>{word_meaning}</rt></ruby>")
                            else:
                                processed_words.append(word)
                            #processed_words.append(f"<span class=\"{self.style}\" data-meaning=\"{self.__query_word(word)}\">{word}</span>")
                        else:
                            processed_words.append(word)
                    else:
                        processed_words.append(word)
                processed_segments.append("".join(processed_words))
        
        return "".join(processed_segments)
    

    # 根据现代词频标注单词
    def by_frequency(self,word_threshold,words,cached_words,):
        '''
        word_threshold: int 现代词频阈值
        words：list 文章中出现次数小于阈值的单词列表
        cached_words: dict 缓存字典
        '''
        segments = self.__split_html()
        processed_segments = []
        for segment in segments:
            if segment.startswith("<"):
                processed_segments.append(segment)
            else:
                paragraph_words = re.split(r"(\s+)", segment)
                processed_words = []
                for word in paragraph_words:
                    new_word = self.__pre_word(word)
                    if new_word in words:
                        if new_word in cached_words:
                            word_freq = cached_words[new_word].get("freq",0)
                            if word_freq>word_threshold:
                                query_result = cached_words[new_word].get("meaning","")
                                if query_result:
                                    processed_words.append(f"<ruby class=\"{self.style}\">{word}<rt>{query_result}</rt></ruby>")
                                else:
                                    processed_words.append(word)
                            else:
                                processed_words.append(word)
                        else:
                            # 如果单词不再缓存中，查询单词释义
                            word_meaning,word_freq = self.__get_word_freq(new_word)
                            # 存入缓存字典
                            cached_words[new_word] = {"meaning":word_meaning,"freq":word_freq}
                            if word_freq>word_threshold:
                                if word_meaning:
                                    processed_words.append(f"<ruby class=\"{self.style}\">{word}<rt>{word_meaning}</rt></ruby>")
                                    
                                else:
                                    processed_words.append(word)
                            else:
                                processed_words.append(word)

                    else:
                        processed_words.append(word)
                processed_segments.append("".join(processed_words))
        
        return "".join(processed_segments),cached_words


    # 获取单词频率
    def __get_word_freq(self,word):
        '''
        word: str
        '''
        word = self.__pre_word(word)
        lemma = self.__query_lemma(word)
        if lemma:
            query_result = self.dict.query(lemma[0])
            wordlen = len(lemma[0])
            if query_result:
                freq = query_result.get("frq",0)
                meaning = self.__process_query_result(query_result,wordlen)
                return meaning,freq
            else:
                return "",0
        query_result = self.dict.query(word)
        wordlen = len(word)
        if query_result:
            freq = query_result.get("frq",0)
            meaning = self.__process_query_result(query_result,wordlen)
            return meaning,freq
        else:
            return "",0
        

    def __pre_word(self,word):
        '''
        word: str
        '''
        return word.strip(".,!?()[]{}").lower().strip()



        