from django.urls import path
from .views import (
    GrievanceListView, GrievanceDetailView, GrievanceCreateView,
    GrievanceAssignView, GrievanceStatusTransitionView
)

app_name = 'grievance'

urlpatterns = [
    path('', GrievanceListView.as_view(), name='grievance_list'),
    path('new/', GrievanceCreateView.as_view(), name='grievance_create'),
    path('<int:pk>/', GrievanceDetailView.as_view(), name='grievance_detail'),
    path('<int:pk>/assign/', GrievanceAssignView.as_view(), name='grievance_assign'),
    path('<int:pk>/transition/', GrievanceStatusTransitionView.as_view(), name='grievance_transition'),
]
