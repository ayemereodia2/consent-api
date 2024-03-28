from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Consent, ConsentPackage
from .models import ConsentSerializer, ConsentPackageSerializer

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