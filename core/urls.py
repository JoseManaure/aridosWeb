from django.contrib import admin
from django.urls import path, include
from core.views import home,pedido
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('orders/', include('orders.urls')),
    path('pedido/', pedido, name='pedido'),
]