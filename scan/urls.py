from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import ScannedView, HomeView, ScanDetailView

app_name = 'scan'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('scanned/', ScannedView.as_view(), name='scanned'),
    path('detail/<int:pk>', ScanDetailView.as_view(), name='detail'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
