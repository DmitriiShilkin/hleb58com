from django.urls import path

from .views import (
    ManagementView,
    StaffListView,
    StaffRegisterView,
    StaffUpdateView,
    StaffAccountView,
    FiredListView,
    staff_remove_view,
    staff_restore_view,
)

urlpatterns = [
    path('', StaffListView.as_view(), name='staff_list'),
    path('signup/', StaffRegisterView.as_view(), name='staff_signup'),
    path('profile/<int:pk>/', StaffUpdateView.as_view(), name='staff_profile'),
    path('account/', StaffAccountView.as_view(), name='staff_account'),
    path('management/', ManagementView.as_view(), name='management'),
    path('remove/<int:pk>/', staff_remove_view, name='staff_remove'),
    path('restore/<int:pk>/', staff_restore_view, name='staff_restore'),
    path('fired/', FiredListView.as_view(), name='fired_list'),
]
