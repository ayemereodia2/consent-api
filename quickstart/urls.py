from django.urls import path
from .views import ConsentDetailView, ConsentPackageAPIView

urlpatterns = [
    path('consent/', ConsentDetailView.as_view(), name='consent-list'),
    path('consent-package', ConsentPackageAPIView.as_view(), name='consentpackage'),
]