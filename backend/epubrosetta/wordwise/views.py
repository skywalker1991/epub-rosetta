from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.core.files.storage import default_storage
import os

# Create your views here.
class Wordwise(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file = request.data['file']
        file_name = default_storage.save(file.name, file)
        file_url = default_storage.url(file_name)
        print(file_url)
        text_frequency = request.data['textFrequency']
        corpus_frequency = request.data['corpusFrequency']
        print(file_name, text_frequency, corpus_frequency)

        static_dir = os.path.join('static','uploads')
        if not os.path.exists(static_dir):
            os.makedirs(static_dir)
        static_file_path = os.path.join(static_dir, file_name)
        with open(static_file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        file_url = request.build_absolute_uri('/static/uploads/' + file_name)

        return Response({'file_url': file_url}, status=status.HTTP_200_OK)
        
