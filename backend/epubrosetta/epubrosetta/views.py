from django.http import FileResponse, HttpResponse
import os
from django.conf import settings

def serve_static_file(request, filename):
    file_path = os.path.join(settings.STATICFILES_DIRS, filename)
    print(file_path,'dddddd')
    response = FileResponse(open(file_path, 'rb'))
    response["Access-Control-Allow-Origin"] = "*"  # 允许跨域访问
    return response