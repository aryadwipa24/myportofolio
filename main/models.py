import uuid
from django.db import models

class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ('internship', 'Internship'),
        ('research', 'Research'),
        ('volunteer', 'Volunteer'),
        ('part-time', 'Part-Time'),
        ('full-time', 'Full-Time'),
        ('freelance', 'Freelance'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='full-time')
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return self.title
    
    @property
    def is_ongoing(self):
        return self.ended_at is None

class Skill(models.Model):
    SKILL_CHOICES = [
        ('programming', 'Programming Language'),
        ('tools', 'Tools & Software'),
        ('language', 'Foreign Language'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=SKILL_CHOICES, default='programmming')
    image = models.CharField(blank=True, null=True)

    def __str__(self):
        return self.title
    
class Education(models.Model):
    EDUCATION_CHOICES = [
        ('pendidikan', 'Pendidikan'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=EDUCATION_CHOICES, default='pendidikan')
    image = models.CharField(blank=True, null=True)
    start = models.DateField()
    end = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def is_ongoing(self):
        return self.end is None

    @property
    def ended(self):
        if self.is_ongoing:
            return "Present"
        return self.end.strftime("%B %Y")