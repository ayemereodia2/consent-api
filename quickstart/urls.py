from django.urls import path
from .views import ConsentDetailView, ConsentPackageAPIView, ConsentPDF,StoredConsentView,StoredGetConsentView

urlpatterns = [
    path('consent/', ConsentDetailView.as_view(), name='consent-list'),
    path('consent-package', ConsentPackageAPIView.as_view(), name='consentpackage'),
    path('consent-pdf/', ConsentPDF.as_view(), name='consent-pdf'),
    path('stored-consents/', StoredConsentView.as_view(), name='stored-consents'),
    path('stored-consents/<str:id>/', StoredGetConsentView.as_view(), name='get_by_id'),
]