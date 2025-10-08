from django.urls import path
from leads import views

app_name = "leads"

urlpatterns = [
    path('', views.LeadListView.as_view(), name='lead-list'),
    path('<int:pk>/', views.LeadDetailView.as_view(), name='lead-detail'),
    path('<int:pk>/update/', views.LeadUpdateView.as_view(), name='lead-update'),
    path('<int:pk>/delete/', views.LeadDeleteView.as_view(), name='lead-delete'),
    path('<int:pk>/assign-agent/', views.AssignAgentView.as_view(), name='assign-agent'),
    path('<int:pk>/category/', views.LeadCategoryUpdateView.as_view(), name='lead-category-update'),
    path('<int:pk>/followups/create/', views.FollowUpCreateView.as_view(), name='lead-followup-create'),
    path('followups/<int:pk>/', views.FollowUpUpdateView.as_view(), name='lead-followup-update'),
    path('followups/<int:pk>/delete/', views.FollowUpDeleteView.as_view(), name='lead-followup-delete'),
    path('create/', views.LeadCreateView.as_view(), name='lead-create'),
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('categories/<int:pk>/update/', views.CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category-delete'),
    path('create-category/', views.CategoryCreateView.as_view(), name='category-create'),
]