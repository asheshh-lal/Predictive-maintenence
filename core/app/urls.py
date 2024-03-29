from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.display_base_html, name='display_base'),
    path('eda', views.render_combined_charts, name='combined_charts'),
    path('customize', views.generate_chart9_data, name='customize_chart'),  
  

] 
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)