import os
from django.shortcuts import render, get_object_or_404, redirect
from main.models import Experience, Skill, Education, Project
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from main.forms import ProjectForm, EducationForm
from functools import wraps

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
            return JsonResponse({'error': 'Unauthorized: Kode rahasia salah/tidak ada!'}, status=403)

        messages.error(request, "Password salah!")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    return _wrapped_view

def show_main(request):
    context = {
        "name": "Arya Dwipa Wicaksana",
        "npm": "2506623111",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Hi! My name is Arya, a third-semester Computer Science student at Universitas Indonesia. "
            "I'm still continuously learning and figuring things out along the way. "
            "I love following my curiosity and deeply exploring the things that catch my interest."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Arya Dwipa Wicaksana",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_skill(request):
    context = {
        "name": "Arya Dwipa Wicaksana",
        "skill_list": Skill.objects.all(),
    }
    return render(request, "skill.html", context)

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
    return render(request, "education.html", context)

@require_secret_key
def create_education(request):
    form = EducationForm(request.POST or None, request.FILES)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pendidikan baru berhasil ditambahkan!")
        return redirect("main:show_education")

    context = {
        "name": "Arya Dwipa Wicaksana",
        "form": form,
    }
    return render(request, "education_form.html", context)

@require_secret_key
def delete_education(request):
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

@require_secret_key
def edit_education(request, education_id):
    education = get_object_or_404(Education, pk=education_id)
    form = EducationForm(request.POST or None, request.FILES, instance=education)

    if request.method == "POST" and form.is_valid():
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
    return render(request, "education_edit_form.html", context)

@require_secret_key
def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "name": "Arya Dwipa Wicaksana",
        "form": form,
    }
    return render(request, "projects_form.html", context)

@require_secret_key
def delete_project(request, project_id):
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
    return render(request, "project.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")