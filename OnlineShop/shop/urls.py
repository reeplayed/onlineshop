from django.urls import path
from .views import shop, detail_view
urlpatterns = [
    path('', shop, name='shop'),
    path('product/<slug:slug>/', detail_view, name='detail-view'),

]