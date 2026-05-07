from django.urls import path
from .views import pedido, dashboard

urlpatterns = [
    path('', pedido, name='pedido'),
    path('dashboard/', dashboard, name='dashboard'),
]