from django.db import models

# Create your models here.

#python manage.py makemigrations Service
# python manage.py migrate

class Service(models.Model):
    name = models.CharField(max_length=320)
    cost = models.IntegerField()
    input_concepts = models.TextField()
    output_concepts = models.TextField()



