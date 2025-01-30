from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.core.files.storage import default_storage
from django.conf import settings
import os
from .epub import Epub
import stat

# Create your views here.
class Wordwise(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file = request.data['file']

        text_frequency = request.data['textFrequency']
        corpus_frequency = request.data['corpusFrequency']
       
        # 将上传的文件保存到media的uploads目录下
        file_name = os.path.join('uploads', file.name)
        file_name = default_storage.save(file_name, file)

        book_settings = {
            'word_show_threshold': int(text_frequency),
            'word_frequency_threshold': int(corpus_frequency),
            'class_name': 'wordwise',
            'english_only': False
        }


        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        # 读取media的uploads目录下的文件, 并处理
        epub = Epub(file_path,book_settings)
        output_filename = epub.process_epub()

        # 处理好的文件的路径
        temp_file = os.path.join(os.path.dirname(__file__), output_filename)

        # 将处理好的文件保存到media的output目录下
        out_book_name = os.path.join('output', output_filename)
        default_storage.save(out_book_name, open(temp_file, 'rb'))
        # 删除处理好的文件
        os.remove(temp_file)

        file_url = request.build_absolute_uri(settings.MEDIA_URL + out_book_name)

        return Response({'file_url': file_url}, status=status.HTTP_200_OK)
        
