from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.parsers import MultiPartParser
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED
from .tasks import upload_large_file_to_s3
from .config_aws import AWS_UPLOAD_BUCKET
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.cache import cache

class FileUploadView(APIView):
    parser_classes = (MultiPartParser,)

    def get(self, request,):
        return render(request, 'upload_file.html')

    def post(self, request, *args, **kwargs):
        file_obj = request.data['file']
        total_number = int(request.data['total_number'])
        part_number = int(request.data['part_number'])
        file_name = str(request.data['file_name'])

        if not file_obj:
            return Response({'error': 'No file was provided.'}, status=HTTP_404_NOT_FOUND)

        bucket_name = AWS_UPLOAD_BUCKET
        key = str(file_name)
        cache.set(f"{file_name}_{part_number}", file_obj.read())

        if cache.get(f"{file_name}_{total_number}"):
            complete_file = b''.join([cache.get(f"{file_name}_{i}") for i in range(1, total_number + 1)])
            upload_large_file_to_s3.delay(complete_file, bucket_name, key)
            for i in range(1, total_number + 1):
                cache.delete(f"{file_name}_{i}")

        return JsonResponse({'message': 'File uploaded'}, status=HTTP_201_CREATED)