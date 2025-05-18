from django.urls import path
from . import views  # Import views from the same folder
from .views import chart_data, add_chart_data, update_chart_data, delete_chart_data  # ✅ Import CRUD functions

urlpatterns = [
    path('', views.home, name='home'),
    path('pie/', views.pie_chart, name='pie_chart'),
    path('bar/', views.bar_chart, name='bar_chart'),
    path('doughnut/', views.doughnut_chart, name='doughnut_chart'),
    path('line/', views.line_chart, name='line_chart'),

    # ✅ API Endpoints
    path('api/chart-data/', chart_data, name='chart_data_api'),
    path('api/chart-data/add/', add_chart_data, name='add_chart_data'),
    path('api/chart-data/update/<int:id>/', update_chart_data, name='update_chart_data'),
    path('api/chart-data/delete/<int:id>/', delete_chart_data, name='delete_chart_data'),
]