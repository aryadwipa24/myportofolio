import os

from django.apps import apps
from django.contrib import messages
from django.core import serializers
from django.templatetags.static import static
from django.views.decorators.http import require_POST
from django.contrib.auth import login, logout
from django.contrib.auth.models import User, Group
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden, Http404

from main.models import Experience, Skill, Education, Project
from main.forms import ProjectForm, EducationForm, SkillForm, ExperienceForm

from functools import wraps
import datetime

MODEL = {
    'experience': 'Experience',
    'skill': 'Skill',
    'education': 'Education',
    'project': 'Project',
}

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

@login_required(login_url="/login/")
def manage_role(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    editor, _ = Group.objects.get_or_create(name="Editor")
    if request.method == 'POST':
        users_non_editor = request.POST.getlist('add_editor')
        users_editor = request.POST.getlist('remove_editor')
        if users_non_editor:
            users_add = User.objects.filter(id__in=users_non_editor)
            for user in users_add:
                user.groups.add(editor)

        if users_editor:
            users_remove = User.objects.filter(id__in=users_editor)
            for user in users_remove:
                user.groups.remove(editor)

        messages.success(request, "Perubahan role berhasil disimpan")

        return redirect('main:manage_role')


    non_editor_query = request.GET.get("search-non-editor", "").strip()
    editor_query = request.GET.get("search-editor", "").strip()
    non_editor = User.objects.exclude(groups=editor).exclude(is_superuser=True)
    editor = User.objects.filter(groups=editor).exclude(is_superuser=True)

    if non_editor_query:
        non_editor = non_editor.filter(username__icontains=non_editor_query)

    if editor_query:
        editor = editor.filter(username__icontains=editor_query)
        
    context = {
        'name': 'Arya Dwipa Wicaksana',
        'non_editor': non_editor,
        'editor': editor,
        'non_editor_query': non_editor_query,
        'editor_query': editor_query,
    }

    return render(request, 'manage_role.html', context)


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
    if not request.user.is_superuser:
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
    if not request.user.is_superuser:
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

@login_required(login_url="/login/")
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
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Arya Dwipa Wicaksana",
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
    educations = Education.objects.prefetch_related('starred_by').all().order_by('-start')

    if title_query:
        educations = educations.filter(title__icontains=title_query)

    data = []
    for education in educations:
        starred_users = education.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ",".join([u.username for u in starred_users])

        data.append({
            "pk": str(education.id),
            "fields": {
                "title": education.title,
                "image": education.image.url if education.image else static("img/no-image.png"),
                "start": education.start.strftime("%B %Y"),
                "end": education.ended,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)

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

@login_required(login_url="/login/")
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

@require_POST
def create_project_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan proyek."},
            status=403,
        )

    form = ProjectForm(request.POST)
    if form.is_valid():
        project = form.save()
        return JsonResponse(
            {"message": "Proyek berhasil ditambahkan.", "pk": str(project.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

@login_required(login_url="/login/")
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
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Arya Dwipa Wicaksana",
        "title_query": title_query,
        "form": ProjectForm(),
    }
    return render(request, "project_templates/project.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.prefetch_related('starred_by').all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    # Konstruksi data JSON secara manual agar bisa menyisipkan logika Star
    data = []
    for project in projects:
        starred_users = project.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "pk": str(project.id),
            "fields": {
                "title": project.title,
                "description": project.description,
                "tech_stack": project.tech_stack,
                "project_url": project.project_url,
                "project_image_url": project.project_image_url,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)

@login_required(login_url="/login/")
def toggle_star(request, model_name, item_id):
    model_name = model_name.lower()
    if model_name not in MODEL:
        raise Http404("Model tidak ditemukan")
    ModelClass = apps.get_model('main', MODEL[model_name])
    item = get_object_or_404(ModelClass, pk=item_id)

    if request.method == "POST":
        if request.user in item.starred_by.all():
            item.starred_by.remove(request.user)
        else:
            item.starred_by.add(request.user)
  
    return redirect(request.META.get('HTTP_REFERER', '/'))