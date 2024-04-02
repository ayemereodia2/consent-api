from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Consent, ConsentPackage, StoredConsent
from .models import ConsentSerializer, ConsentPackageSerializer, SignedConsentSerializer, StoredConsentSerializer
from rest_framework.views import APIView
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from io import BytesIO
from django.core.files.base import ContentFile
import os
import boto3
from botocore.exceptions import ClientError
import random
import string
import json

class ConsentDetailView(APIView):
    def get(self, request, consent_id):
        consent = Consent.objects.get(pk=consent_id)
        serializer = ConsentSerializer(consent)
        return Response(serializer.data)

    def post(self, request):
        serializer = ConsentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        consents = Consent.objects.all()
        serializer = ConsentSerializer(consents, many=True)
        return Response(serializer.data)
    
    


class ConsentPackageAPIView(APIView):
    def get(self, request):
        consent_packages = ConsentPackage.objects.all()
        serializer = ConsentPackageSerializer(consent_packages, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ConsentPackageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    

class ConsentPDF(APIView):
    def post(self, request):
        # Deserialize request data
        serializer = SignedConsentSerializer(data=request.data)
        if serializer.is_valid():
            # Assuming the serializer validates the data correctly
            # You may want to process the data further or save it to the database
            # Get data from serializer
            consent_data = serializer.validated_data
            # Render the PDF
            pdf_content = self.render_to_pdf('signed-consent.html', context_dict= consent_data)
            key = self.generate_random_string() + 'consent.pdf'
            response_from_s3 = self.upload_to_s3(pdf_content, 'hsns-bucket', key)
            
            # Return PDF as HTTP response
            response = HttpResponse(pdf_content, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="consent.pdf"'
            return response
        return Response({"error": serializer.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get(self, request):
        result = self.fetch_all_documents(bucket_name='hsns-bucket')
        if result:
            return Response(result, status=status.HTTP_200_OK)
        return Response([], status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    def render_to_pdf(self, template_src, context_dict):
        template = get_template(template_src)
        html = template.render(context_dict)
        
        # Creating a PDF file
        pdf_content = BytesIO()
        pisa_status = pisa.CreatePDF(html, dest=pdf_content)
        if pisa_status.err:
            return HttpResponse('Failed to generate PDF: %s' % pisa_status.err)
        return pdf_content.getvalue()
    
    def upload_to_s3(self, file_content, bucket_name, object_name):
        """
        Uploads a file to an S3 bucket.

        :param file_content: The content of the file to upload.
        :param bucket_name: The name of the S3 bucket.
        :param object_name: The name of the object in the S3 bucket.
        :return: True if the file was uploaded successfully, else False.
        """
        try:
            # Create an S3 client
            s3_client = boto3.client('s3', aws_access_key_id="AKIAVRUVP243WUV2M44K",
         aws_secret_access_key= "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")

            # Upload the file
            response = s3_client.put_object(Body=file_content, Bucket=bucket_name, Key=object_name)
            print("S3 response", response)
        except ClientError as e:
            print(f"Failed to upload file to S3: {e}")
            return False
        return True
    
    def fetch_all_documents(self, bucket_name):
        # List all objects in the bucket
        result = []
        s3_client = boto3.client('s3', aws_access_key_id="AKIAVRUVP243WUV2M44K",
         aws_secret_access_key= "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")
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        
        content = self.parse_aws_response(response)
        # Check if there are any objects in the bucket
        if content:
            for item in content:
                key = item.get('Key', '')
                result.append(f'https://hsns-bucket.s3.us-west-2.amazonaws.com/{key}')
            
            return result
        else:
            # No objects found in the bucket
            return []
    
    
    def generate_random_string(self, length = 6):
        """Generate a random alphanumeric string of specified length."""
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))
    
    def parse_aws_response(self, json_data):
        # Access the 'Contents' object
        contents = json_data.get('Contents', [])
        return contents
    
    
class StoredConsentView(APIView):
    def get(self, request):
        consent_packages = StoredConsent.objects.all()
        serializer = StoredConsentSerializer(consent_packages, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = StoredConsentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
class StoredGetConsentView(APIView):
    def get(self, request, id):
        try:
            consent_package = StoredConsent.objects.get(pk=id)
            #consent_package = StoredConsent.objects.filter(health_card_number=health_card_number)
            serializer = StoredConsentSerializer(consent_package)
            return Response(serializer.data)
        except StoredConsent.DoesNotExist:
            return Response({'error': 'StoredConsent not found'}, status=status.HTTP_404_NOT_FOUND)