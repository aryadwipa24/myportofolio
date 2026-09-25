import os

from django.contrib import messages
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth import login, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from main.models import Experience, Skill, Education, Project
from main.forms import ProjectForm, EducationForm, SkillForm, ExperienceForm

from functools import wraps
import datetime

SECRET_KEY = os.getenv("SECRET_API_KEY", "HewanHewanApaYangSatuKata?")

def require_secret_key(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.method == 'GET':
            return view_func(request, *args, **kwargs)
        
        header_key = request.META.get("HTTP_X_SECRET_KEY")
        form_key = request.POST.get("secret_password")

        if header_key == SECRET_KEY or form_key == SECRET_KEY:
            return view_func(request, *args, **kwargs)

        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'api' in request.path:
            return JsonResponse({'error': 'Password salah!'}, status=403)

        messages.error(request, "Password salah!")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    return _wrapped_view

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Arya Dwipa Wicaksana",
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Arya Dwipa Wicaksana",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie("last_login")
    return response

def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        "name": "Arya Dwipa Wicaksana",
        "npm": "2506623111",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Hi! My name is Arya, a third-semester Computer Science student at Universitas Indonesia. "
            "I'm still continuously learning and figuring things out along the way. "
            "I love following my curiosity and deeply exploring the things that catch my interest."
        ),
        "last_login": last_login,
    }
    return render(request, "index.html", context)


def show_experience(request):
    json_response = get_experience_json(request)

    experiences = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8")
    )
    experiences = [experience.object for experience in experiences]
    experiences = sorted(experiences, key=lambda x: x.id)
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Arya Dwipa Wicaksana",
        "experience_list": experiences,
        "title_query": title_query,
    }
    return render(request, "experience_templates/experience.html", context)

@login_required(login_url="/login/")
def create_experience(request):
    if not request.user.is_super:
        raise PermissionDenied
    
    form = ExperienceForm(request.POST or None, request.FILES)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman baru berhasil ditambahkan!")
        return redirect("main:show_experience")

    context = {
        "name": "Arya Dwipa Wicaksana",
        "form": form,
    }
    return render(request, "experience_templates/experience_form.html", context)

@login_required(login_url="/login/")
def delete_experience(request):
    if not request.user.is_super:
        raise PermissionDenied
    
    experience_ids = request.POST.getlist("selected_experiences")

    if request.method == "POST":
        Experience.objects.filter(id__in=experience_ids).delete()
        messages.success(request, f"{len(experience_ids)} pengalaman berhasil dihapus!")
        return redirect("main:show_experience")

    return redirect("main:show_experience")

def get_experience_json(request):
    title_query = request.GET.get("title", "").strip()
    experience = Experience.objects.all()

    if title_query:
        experience = experience.filter(title__icontains=title_query)

    experience_json = serializers.serialize("json", experience)
    return HttpResponse(experience_json, content_type="application/json")

@login_required(login_url="/login/")
def edit_experience(request, experience_id):
    is_editor = request.user.groups.filter(name='Editor').exists()
    is_superuser = request.user.is_superuser

    if not (is_editor or is_superuser):
        raise PermissionDenied
    
    experience = get_object_or_404(Experience, pk=experience_id)
    form = ExperienceForm(request.POST or None, request.FILES, instance=experience)

    if request.method == "POST" and form.is_valid():
        if request.POST.get("image-clear"):
            experience.thumbnail = None
        form.save()
        messages.success(request, "Pengalaman berhasil diperbarui!")
        return redirect("main:show_experience")
    else:
        form = ExperienceForm(instance=experience)

    context = {
            "name": "Arya Dwipa Wicaksana",
            "form": form,
            'experience': experience
        }
    return render(request, "experience_templates/experience_edit_form.html", context)

def show_skill(request):
    json_response = get_skill_json(request)
    
    skills = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    skills = [skill.object for skill in skills]
    order = ["programming", "tools", "language"]
    skills = sorted(skills, key=lambda x: order.index(x.category) if x.category in order else 99)
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Arya Dwipa Wicaksana",
        "skill_list": skills,
        "title_query": title_query,
    }
    return render(request, "skill_templates/skill.html", context)

@login_required(login_url="/login/")
def create_skill(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    form = SkillForm(request.POST or None, request.FILES)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Skill baru berhasil ditambahkan!")
        return redirect("main:show_skill")

    context = {
        "name": "Arya Dwipa Wicaksana",
        "form": form,
    }
    return render(request, "skill_templates/skill_form.html", context)

@login_required(login_url="/login.")
def delete_skill(request):
    if not request.user.is_superuser:
            raise PermissionDenied
    
    skill_ids = request.POST.getlist("selected_skills")

    if request.method == "POST":
        Skill.objects.filter(id__in=skill_ids).delete()
        messages.success(request, f"{len(skill_ids)} skill berhasil dihapus!")
        return redirect("main:show_skill")

    return redirect("main:show_skill")

def get_skill_json(request):
    title_query = request.GET.get("title", "").strip()
    skill = Skill.objects.all()

    if title_query:
        skill = skill.filter(title__icontains=title_query)

    skill_json = serializers.serialize("json", skill)
    return HttpResponse(skill_json, content_type="application/json")

@login_required(login_url="/login/")
def edit_skill(request, skill_id):
    is_editor = request.user.groups.filter(name='Editor').exists()
    is_superuser = request.user.is_superuser

    if not (is_superuser or is_editor):
        raise PermissionDenied
    
    skill = get_object_or_404(Skill, pk=skill_id)
    form = SkillForm(request.POST or None, request.FILES, instance=skill)

    if request.method == "POST" and form.is_valid():
        if request.POST.get("image-clear"):
            if skill.image:
                skill.image.delete(save=False)
            skill.image = None
        form.save()
        messages.success(request, "Skill berhasil diperbarui!")
        return redirect("main:show_skill")
    else:
        form = SkillForm(instance=skill)

    context = {
            "name": "Arya Dwipa Wicaksana",
            "form": form,
            'skill': skill
        }
    return render(request, "skill_templates/skill_edit_form.html", context)

def show_education(request):
    json_response = get_education_json(request)

    educations = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    educations = [education.object for education in educations]
    educations = sorted(educations, key=lambda x: x.start, reverse=True)
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Arya Dwipa Wicaksana",
        "education_list": educations,
        "title_query": title_query,
    }
    return render(request, "education_templates/education.html", context)

@login_required(login_url="/login/")
def create_education(request):
    if not request.user.is_superuser:
            raise PermissionDenied
    
    form = EducationForm(request.POST or None, request.FILES)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pendidikan baru berhasil ditambahkan!")
        return redirect("main:show_education")

    context = {
        "name": "Arya Dwipa Wicaksana",
        "form": form,
    }
    return render(request, "education_templates/education_form.html", context)

@login_required(login_url=".login/")
def delete_education(request):
    if not request.user.is_superuser:
            raise PermissionDenied
    
    education_ids = request.POST.getlist("selected_educations")

    if request.method == "POST":
        Education.objects.filter(id__in=education_ids).delete()
        messages.success(request, f"{len(education_ids)} riwayat pendidikan berhasil dihapus!")
        return redirect("main:show_education")

    return redirect("main:show_education")

def get_education_json(request):
    title_query = request.GET.get("title", "").strip()
    education = Education.objects.all()

    if title_query:
        education = education.filter(title__icontains=title_query)

    education_json = serializers.serialize("json", education)
    return HttpResponse(education_json, content_type="application/json")

@login_required(login_url="/login/")
def edit_education(request, education_id):
    is_editor = request.user.groups.filter(name='Editor').exists()
    is_superuser = request.user.is_superuser

    if not (is_editor or is_superuser):
        raise PermissionDenied
    
    education = get_object_or_404(Education, pk=education_id)
    form = EducationForm(request.POST or None, request.FILES, instance=education)

    if request.method == "POST" and form.is_valid():
        if request.POST.get("image-clear"):
            if education.image:
                education.image.delete(save=False)
            education.image = None
        form.save()
        messages.success(request, "Pendidikan berhasil diperbarui!")
        return redirect("main:show_education")
    else:
        form = EducationForm(instance=education)

    context = {
            "name": "Arya Dwipa Wicaksana",
            "form": form,
            'education': education
        }
    return render(request, "education_templates/education_edit_form.html", context)

@login_required
def create_project(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "name": "Arya Dwipa Wicaksana",
        "form": form,
    }
    return render(request, "project_templates/projects_form.html", context)

@login_required
def delete_project(request, project_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")

def show_projects(request):
    json_response = get_projects_json(request)

    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [project.object for project in projects]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Arya Dwipa Wicaksana",
        "project_list": projects,
        "title_query": title_query,
    }
    return render(request, "project_templates/project.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects, use_natural_foreign_keys=True)
    return HttpResponse(projects_json, content_type="application/json")

@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)
  
    return redirect("main:show_projects")