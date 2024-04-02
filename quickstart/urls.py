from django.urls import path
from .views import ConsentDetailView, ConsentPackageAPIView, ConsentPDF

urlpatterns = [
    path('consent/', ConsentDetailView.as_view(), name='consent-list'),
    path('consent-package', ConsentPackageAPIView.as_view(), name='consentpackage'),
    path('consent-pdf/', ConsentPDF.as_view(), name='consent-pdf'),
]