from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from chatMessages import views


urlpatterns = [
    path('messages/', views.MessageList.as_view()),
    path('message/<int:pk>/', views.MessageDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)