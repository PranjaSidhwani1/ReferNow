from django.db import models
from django.conf import settings
import uuid
from django.db import models
from django.conf import settings


import uuid

class ReferralPost(models.Model):

    job_id = models.CharField(max_length=50)

    referrer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='referral_posts'
    )

    company = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    description = models.TextField()
    available_slots = models.IntegerField(default=1)

    is_open = models.BooleanField(default=True)  # NEW FIELD

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        self.available_slots = int(self.available_slots)  # 🔥 force int

        if self.available_slots <= 0:
            self.available_slots = 0
            self.is_open = False

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.company} - {self.job_title}"


class ReferralApplication(models.Model):

    STATUS_CHOICES = (
        ('applied', 'Applied'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('referred', 'Referred'),
    )

    referral_post = models.ForeignKey(
        ReferralPost,
        on_delete=models.CASCADE,
        related_name='applications'
    )

    candidate = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='referral_applications'
    )

    message = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='applied'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidate.username} -> {self.referral_post.company}"
    



class Referral(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    description = models.TextField()
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Application(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    ]

    referral = models.ForeignKey(ReferralPost, on_delete=models.CASCADE)
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    resume = models.FileField(upload_to='resumes/')

    why_refer = models.TextField()
    why_company = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    chat_enabled = models.BooleanField(default=False)  # 🔥 ADD THIS

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('referral', 'applicant')

class ChatMessage(models.Model):
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.message[:20]}"