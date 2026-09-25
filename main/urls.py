from django.urls import path

from main.views import (show_main, 
                        show_experience, create_experience, delete_experience, get_experience_json, edit_experience,
                        show_skill, create_skill, delete_skill, get_skill_json, edit_skill,
                        show_education, create_education, delete_education, get_education_json, edit_education,
                        show_projects, create_project, delete_project, get_projects_json, toggle_star,
                        register, login_user, logout_user,)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("experience/add/", create_experience, name="create_experience"),
    path("experience/delete/",delete_experience,name="delete_experience"),
    path("api/experience/", get_experience_json, name="get_experience_json"),
    path("experience/<uuid:experience_id>/edit/", edit_experience, name="edit_experience"),

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
    path("projects/<uuid:project_id>/star/", toggle_star, name="toggle_star"),

    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout")
]