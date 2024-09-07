from django.urls import path
from .views import AskView

urlpatterns = [
    path('api/ask/', AskView.as_view(), name='ask_gpt'),
]
