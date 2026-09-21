from django.forms import ModelForm, TextInput, Textarea, URLInput, DateInput, ClearableFileInput
from django import forms
from main.models import Project, Education, Skill, Experience

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "tech_stack",
            "project_url",
            "project_image_url",
        ]

        labels = {
            "title": "Nama Proyek",
            "description": "Deskripsi Proyek",
            "tech_stack": "Teknologi yang Digunakan",
            "project_url": "URL Proyek",
            "project_image_url": "URL Gambar Proyek",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Portfolio Website",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan Proyekmu",
                    "rows": 3,
                }
            ),
            "tech_stack": TextInput(
                attrs={
                    "placeholder": "Django, Python, HTML, CSS",
                }
            ),
            "project_url": URLInput(
                attrs={
                    "placeholder": "https://github.com/kakBurhan/burhanquestv4",
                }
            ),
            "project_image_url": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
        }

class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = [
            "title",
            "start",
            "end",
            "image",
        ]

        labels = {
            "title": "Nama Institusi Pendidikan",
            "start": "Tahun Memulai",
            "end": "Tahun Selesai (Jika Masih Berlangsung Kosongkan Saja)",
            "image": "Foto Lambang Institusi Pendidikan (Opsional)",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Nama Institusi Pnedidikan",
                    "maxlength": 255,
                }
            ),
            'start': forms.DateInput(
                format='%Y-%m',
                attrs={'type': 'month',}
            ),
            'end': forms.DateInput(
                format='%Y-%m',
                attrs={'type': 'month',}
            ),
            "image": forms.FileInput(
                attrs={
                    "accept": "image/*",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start'].input_formats = ['%Y-%m', '%Y-%m-%d']
        self.fields['end'].input_formats = ['%Y-%m', '%Y-%m-%d']

class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = [
            "title",
            "category",
            "image",
        ]

        labels = {
            "title": "Nama Skill",
            "category": "Bidang Skill",
            "image": "Foto Skill (Opsional)",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Nama Skill",
                    "maxlength": 255,
                }
            ),
            'category': forms.Select(
                choices=Skill.SKILL_CHOICES,
            ),
            "image": forms.FileInput(
                attrs={
                    "accept": "image/*",
                }
            ),
        }

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            "title",
            "description",
            "category",
            "thumbnail",
            "started_at",
            "ended_at",
        ]

        labels = {
            "title": "Nama Pengalaman",
            "description": "Deskripsi Pengalaman",
            "category": "Kategori Pengalaman",
            "thumbnail": "URL Gambar Pengalaman (Opsional)",
            "started_at": "Tanggal Mulai",
            "ended_at": "Tanggal Selesai (Opsional)",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Nama Pengalaman",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan Pengalaman",
                    "rows": 3,
                }
            ),
            'category': forms.Select(
                choices=Experience.EXPERIENCE_CHOICES,
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
            "started_at": forms.DateTimeInput(
                attrs={
                    "type": "date"
                },
                format="%Y-%m-%d",
            ),
            "ended_at": forms.DateTimeInput(
                attrs={
                    "type": "date"
                },
                format="%Y-%m-%d",
            ),            
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.started_at:
                self.fields['started_at'].widget.format = '%Y-%m-%d'
            if self.instance.ended_at:
                self.fields['ended_at'].widget.format = '%Y-%m-%d'