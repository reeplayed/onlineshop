
from django.contrib import admin
from django.urls import path, include
from account.views import home, registration
from cart.views import cart
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from billing.views import checkout

urlpatterns = [
    path('', home, name='home'),
    path('registration/', registration, name='registration'),
    path('checkout/', checkout, name='checkout'),
    path('cart/', cart, name='cart'),
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='account/logout.html'), name='logout'),
    path('shop/', include('shop.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
