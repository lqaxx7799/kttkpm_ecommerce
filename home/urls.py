from django.urls import path
from . import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<str:type>/<int:theloai>', views.category_products, name='category_products'),
    path('search/', views.search, name='search')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
