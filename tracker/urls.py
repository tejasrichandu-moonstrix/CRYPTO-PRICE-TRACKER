
from django.urls import path
from . import views

app_name = 'tracker'

urlpatterns = [
    path('', views.index, name='index'),
    path('history/<int:crypto_id>/', views.price_history, name='price_history'),
    path('api/refresh/<int:crypto_id>/', views.api_refresh_price, name='api_refresh_price'),
]