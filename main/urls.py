from django.urls import path

from main.views import (show_main, 
                        show_experience, 
                        show_skill, create_skill, delete_skill, get_skill_json, edit_skill,
                        show_education, create_education, delete_education, get_education_json, edit_education,
                        show_projects, create_project, delete_project, get_projects_json,)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),

    path("skill/", show_skill, name="show_skill"),
    path("skill/add/", create_skill, name="create_skill"),
    path("skill/delete/",delete_skill,name="delete_skill"),
    path("api/skill/", get_skill_json, name="get_skill_json"),
    path("skill/<uuid:skill_id>/edit/", edit_skill, name="edit_skill"),

    path("education/", show_education, name="show_education"),
    path("education/add/", create_education, name="create_education"),
    path("education/delete/",delete_education,name="delete_education"),
    path("api/education/", get_education_json, name="get_education_json"),
    path("education/<uuid:education_id>/edit/", edit_education, name="edit_education"),

    path("projects/", show_projects, name="show_projects"),
    path("projects/add/", create_project, name="create_project"),
    path("projects/<uuid:project_id>/delete/",delete_project,name="delete_project"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
]