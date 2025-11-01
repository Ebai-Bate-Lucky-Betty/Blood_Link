from django.urls import path
from .views import NotificationListView, MarkAllReadView, NotificationDeleteView

urlpatterns = [
    path('list/', NotificationListView.as_view(), name='notifications-list'),
    path('mark-all-read/', MarkAllReadView.as_view(), name='notifications-mark-all-read'),
    path('<int:pk>/delete/', NotificationDeleteView.as_view(), name='notifications-delete'),
]
