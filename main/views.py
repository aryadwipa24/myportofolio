from django.shortcuts import render

from main.models import Experience


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