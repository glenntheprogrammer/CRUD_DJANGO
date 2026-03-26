from django.urls import path
from . import views

urlpatterns = [
    # Page
    path('', views.list_page, name='profile_list'),

    # AJAX
    path('ajax/list/', views.list_ajax, name='list_ajax'),
    path('ajax/get/<int:pk>/', views.get_ajax, name='get_ajax'),
    path('ajax/save/', views.save_ajax, name='save_ajax'),
    path('ajax/delete/<int:pk>/', views.delete_ajax, name='delete_ajax'),
]