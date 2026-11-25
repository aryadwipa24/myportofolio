from django.urls import path
from main import api_views
from rest_framework.authtoken import views as authtoken_views

app_name = "api"
urlpatterns = [
    path("projects/", api_views.project_list, name="project-list"),
    path("projects/<uuid:project_id>/", api_views.project_detail, name="project-detail"),
    path("projects/<uuid:project_id>/star/", api_views.project_star, name="project-star"),
    
    path("educations/", api_views.education_list, name="education-list"),
    path("educations/<uuid:education_id>/", api_views.education_detail, name="education-detail"),
    path("educations/<uuid:education_id>/star/", api_views.education_star, name="education-star"),

    path("auth/token/", authtoken_views.obtain_auth_token, name="api_token_auth"),
    path('auth/logout/', api_views.api_logout, name="api_logout"),
]