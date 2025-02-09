import zipfile
import os
import shutil
import nltk
from bs4 import BeautifulSoup
from .stardict import StarDict, LemmaDB
from .wordwise import Wordwise
import os


# 创建Epub文件处理类

class Epub:
    def __init__(self, epub_file_path,settings={}):
        self.epub_file = epub_file_path
        self.epub_file_name = os.path.basename(epub_file_path)
        # 解压后的文件存储目录，当前代码文件所处目录下的epub_contents文件夹
        self.current_dir = os.path.dirname(__file__)
        self.output_contents_dir = os.path.join(self.current_dir, "epub_contents") 
        # 生成的epub文件名为原文件名加上_processed
        # 获取文件不带路径的文件名
        epub_file = os.path.basename(epub_file_path)
        self.output_epub_file = os.path.join(self.current_dir,os.path.splitext(epub_file)[0] + "_processed.epub")
        self.settings = settings

    def extract_epub(self):
        with zipfile.ZipFile(self.epub_file, 'r') as zip_ref:
            zip_ref.extractall(self.output_contents_dir)
        print(f"EPUB 解压完成，文件已存储在 {self.output_contents_dir}")


    # 使用beautifulsoup统计全文单词频率
    def get_epub_word_freq(self):
        text = ''
        for root, dirs, files in os.walk(self.output_contents_dir):
            for file in files:
                if file.endswith(".xhtml") or file.endswith(".html") or file.endswith(".xml"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8") as f:
                        html_content = f.read()
                    soup = BeautifulSoup(html_content, 'html.parser')
                    text += soup.get_text()
        tokens = nltk.word_tokenize(text)
        # 去除标点符号
        tokens = [word for word in tokens if word.isalnum()]
        # 将单词转换为小写
        tokens = [word.lower() for word in tokens]
        fdist = nltk.FreqDist(tokens)
        return fdist
    
    # 找出全文中出现次数小于threshold的单词列表
    def get_rare_words(self, threshold=2):
        fdist = self.get_epub_word_freq()
        rare_words = [word for word, freq in fdist.items() if freq < threshold]
        return rare_words

    def process_html_files(self):
        if self.settings.get('word_frequency_threshold') == 0:
            self.word_wise_by_word()
        else:
            self.word_wise_by_frequency()

            


    def word_wise_by_word(self):
        # 根据settings中的word_show_threshold参数，找出全文中出现次数小于threshold的单词列表
        if self.settings.get('word_show_threshold') == 0:
            rare_words = self.get_rare_words()
        else:
            rare_words = self.get_rare_words(self.settings.get('word_show_threshold'))
        # 初始化离线词典
        db = os.path.join(os.path.dirname(__file__), 'test.db')
        dict = StarDict(db,False)
        # 读取epub文件中的章节内容, 并为每个稀有词汇添加可以在kindle上显示的释义
        for root, dirs, files in os.walk(self.output_contents_dir):
            for file in files:
                if file.endswith(".xhtml"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8") as f:
                        html_content = f.read()
                    wordwise = Wordwise(dict,html_content,self.settings.get('class_name'))
                    wordwised_html = wordwise.by_word(rare_words)
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(wordwised_html)

        return True
    
    
    # 根据settings中的word_frequency_threshold参数，找出全文的单词频率排位在threshold之后的单词列表
    def word_wise_by_frequency(self):
        # 根据settings中的word_show_threshold参数，找出全文中出现次数小于threshold的单词列表
        if self.settings.get('word_show_threshold') == 0:
            rare_words = self.get_rare_words()
        else:
            rare_words = self.get_rare_words(self.settings.get('word_show_threshold'))
        # 初始化离线词典
        db = os.path.join(os.path.dirname(__file__), 'test.db')
        dict = StarDict(db,False)

        # 初始化lemma词典
        lemma = LemmaDB()
        # 加载lemma词典，在当前目录下有一个lemma.en.txt文件，里面存放了英文单词的原型
        lemma_file = os.path.join(os.path.dirname(__file__), 'lemma.en.txt')
        
        lemma.load(lemma_file)
        



        # 读取epub文件中的章节内容, 并为每个稀有词汇添加可以在kindle上显示的释义
        for root, dirs, files in os.walk(self.output_contents_dir):
            cached_dict = {}
            for file in files:
                # 文件后缀可能为xhtml或者html或xml
                if file.endswith(".xhtml") or file.endswith(".html") or file.endswith(".xml"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8") as f:
                        html_content = f.read()
                    wordwise = Wordwise(dict,lemma,html_content,self.settings.get('class_name'))
                    wordwised_html,cached_dict = wordwise.by_frequency(self.settings.get('word_frequency_threshold'),rare_words,cached_dict)
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(wordwised_html)



    
    
    
    #给epub文件css添加样式
    def add_css(self):
        css_file = os.path.join(os.path.dirname(__file__), 'style.css')
        for root, dirs, files in os.walk(self.output_contents_dir):
            for file in files:
                if file.endswith(".css"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "a", encoding="utf-8") as f:
                        with open(css_file, "r", encoding="utf-8") as css:
                            f.write(css.read())
        return True
    

    def compress_epub(self):
        shutil.make_archive(self.output_epub_file, 'zip', self.output_contents_dir)
        os.rename(self.output_epub_file + ".zip", self.output_epub_file)
        print("EPUB 文件压缩完成,文件已存储在", self.output_epub_file)
        # 删除解压后的文件夹内容
        shutil.rmtree(self.output_contents_dir)
        # 返回生成的epub文件名
        final_epub_file = os.path.basename(self.output_epub_file)
        return final_epub_file

    def process_epub(self):
        self.extract_epub()
        self.add_css()
        self.process_html_files()
        output_file_name = self.compress_epub()
        return output_file_name


if __name__ == "__main__":
    # 解压 EPUB 文件
    epub_file = "input.epub"
    output_dir = "epub_contents"
    settings = {'word_show_threshold': 10,'word_frequency_threshold': 10000,'class_name': 'wordwise','english_definition': False}
    epub = Epub(epub_file,settings)
    epub.process_epub()

