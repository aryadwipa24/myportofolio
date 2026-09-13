from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Skill, Education
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )

        self.dummy_image = SimpleUploadedFile(
            name='test_image.png',
            content=b'\x47\x49\x46\x89\x50\x4e\x47\x0d\x0a\x1a\x0a',
            content_type='image/png'
        )

        self.skill = Skill.objects.create(
            title="Java",
            category="programming",
            image=self.dummy_image,
        )
        self.education = Education.objects.create(
            title="Universitas Indonesia",
            category="pendidikan",
            image=self.dummy_image,
            start=date(2025, 8, 1),
        )


    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Selesai")
        self.assertNotContains(response, "Sedang berlangsung")

    def test_skill_model(self):
        self.assertEqual(str(self.skill), "Java")
        self.assertEqual(self.skill.category, "programming")
        self.assertTrue(self.skill.image)
        self.assertIn("test_image", self.skill.image.name)

    def test_skill_page(self):
        response = self.client.get(reverse("main:show_skill"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "skill.html")
        self.assertContains(response, self.skill.title)
        self.assertContains(response, self.skill.image.url)
        self.assertContains(response, f'href="{reverse("main:show_main")}"')
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')
        self.assertContains(response, f'href="{reverse("main:show_education")}"')

    def test_empty_skill_page(self):
        Skill.objects.all().delete()
        response = self.client.get(reverse("main:show_skill"))

        self.assertContains(response, "Belum ada skill yang ditambahkan.")
        
    def test_education_model(self):
        self.assertEqual(str(self.education), "Universitas Indonesia")
        self.assertEqual(self.education.category, "pendidikan")
        self.assertTrue(self.education.image)
        self.assertIn("test_image", self.education.image.name)
        self.assertEqual(self.education.start, date(2025, 8, 1))
        self.assertTrue(self.education.is_ongoing)
        self.assertEqual(self.education.ended, "Present")

    def test_education_page(self):
        response = self.client.get(reverse("main:show_education"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "education.html")
        self.assertContains(response, self.education.title)
        self.assertContains(response, self.education.image.url)
        self.assertContains(response, f'href="{reverse("main:show_main")}"')
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')
        self.assertContains(response, f'href="{reverse("main:show_skill")}"')

    def test_empty_education_page(self):
        Education.objects.all().delete()
        response = self.client.get(reverse("main:show_education"))

        self.assertContains(response, "Belum ada pendidikan yang ditambahkan.")

    def test_completed_education(self):
            self.education.end = timezone.now()
            self.education.save()
            response = self.client.get(reverse("main:show_education"))
    
            self.assertFalse(self.education.is_ongoing)
            self.assertContains(response, timezone.now().strftime("%B %Y"))
            self.assertNotContains(response, "Present")
