from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # path('', views.render_combined_charts, name='combined_charts'),  

] 
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)