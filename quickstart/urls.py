from django.urls import path
from .views import ConsentDetailView

urlpatterns = [
    path('consent/', ConsentDetailView.as_view(), name='consent-list'),
]