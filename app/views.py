from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED
from rest_framework.views import APIView
from .models import Document
from .tasks import upload_large_file_to_s3
from .config_aws import AWS_UPLOAD_BUCKET



class FileUploadView(APIView):
    parser_classes = (MultiPartParser,)

    def get(self, request,):
        return render(request, 'upload_file.html')


    def post(self, request, *args, **kwargs):
        file_obj = request.data['file']

        if not file_obj:
            return Response({'error': 'No file was provided.'}, status=HTTP_404_NOT_FOUND)

        file_model = Document()
        file_model.file_name = file_obj.name
        file_model.file_extension = file_obj.name[1]
        file_model.save()

        bucket_name = AWS_UPLOAD_BUCKET
        key = str(file_model.id) + ' ' + str(file_obj.name)
        file_data = file_obj.read()
        print("FILE TYPE", type(file_data))
        upload_large_file_to_s3.delay(file_data, bucket_name, key)

        return JsonResponse({'message': 'File uploaded'}, status=HTTP_201_CREATED)











































# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework.parsers import MultiPartParser
# from rest_framework.response import Response
# from .tasks import process_and_upload_file
# from .models import Document
#
# class FileUploadView(APIView):
#     parser_classes = (MultiPartParser,)
#
#     def get(self, request,):
#         # Render the upload template for GET requests
#         return render(request, 'upload_file.html')
#
#     def post(self, request, *args, **kwargs):
#         # uploaded_file = request.FILES['file']
#         uploaded_file = request.data['file']
#         print("uploaded file", uploaded_file)
#
#
#         # Create a new instance of your model and save the uploaded file
#         file_model = Document()
#         file_model.file_name = uploaded_file.name
#         file_model.file_extension = uploaded_file.name.split('.')[-1]  # Extract extension
#         file_model.save()
#         print("FILE MODEL ID", file_model.id)
#
#
#         # Enqueue the file processing and uploading task using Celery
#         process_and_upload_file.apply_async(args=(file_model.id, uploaded_file))
#
#         return Response({'message': 'File uploaded and processing started.'})
