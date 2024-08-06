from django.db import models
from hashlib import sha256


def custom_qn_src_upload_to(instance, filename):
    hash = sha256(f"{instance.title}{instance.created_at}".encode(
        'utf-8')).hexdigest()
    return f'qn_src/{hash}.{filename.split(".")[-1]}'


def custom_qn_config_upload_to(instance, filename):
    hash = sha256(f"{instance.title}{instance.created_at}".encode(
        'utf-8')).hexdigest()
    return f'qn_config/{hash}.{filename.split(".")[-1]}'


def custom_qn_test_upload_to(instance, filename):
    hash = sha256(f"{instance.title}{instance.created_at}".encode(
        'utf-8')).hexdigest()
    return f'qn_test/{hash}.{filename.split(".")[-1]}'


class Question(models.Model):

    difficulty_choices = (
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    )

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    body = models.TextField()
    config = models.FileField(
        upload_to=custom_qn_config_upload_to, null=True, blank=True)
    src_files_zip = models.FileField(
        upload_to=custom_qn_src_upload_to, null=True, blank=True)
    test = models.FileField(
        upload_to=custom_qn_test_upload_to, null=True, blank=True)
    docker_image = models.CharField(max_length=256, null=True, blank=True)
    description = models.TextField()
    difficulty = models.CharField(
        max_length=10, choices=difficulty_choices, default='Easy')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Create your models here.
