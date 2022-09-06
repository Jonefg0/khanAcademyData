from django.db import models

# Create your models here.
class Logros(models.Model):
    id = models.AutoField(primary_key=True)
    codigo_escuela = models.CharField(max_length=255)
    numero_estudiantes = models.CharField(max_length=255)
    fecha_script = models.CharField(max_length=255)
    fecha_inicio = models.CharField(max_length=255)
    fecha_fin = models.CharField(max_length=255)
    numero_semana = models.CharField(max_length=255)
    suma_minutos = models.CharField(max_length=255)
    skills_mejoradas = models.CharField(max_length=255)
    suma_skill_sin_avance = models.CharField(max_length=255)
    maximo_ejercicios = models.CharField(max_length=255)
    maximo_skills = models.CharField(max_length=255)
