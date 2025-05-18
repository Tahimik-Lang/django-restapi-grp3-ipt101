from django.contrib import admin
from django.urls import path, include
from dept1 import views  # Import your home view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dept1/', include('dept1.urls')),
    path('', views.home, name='home'),  # ✅ Add this line to route the root URL
]