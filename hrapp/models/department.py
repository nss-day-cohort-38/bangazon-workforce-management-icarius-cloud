from django.db import models
from django.urls import reverse

class Department(models.Model):

    name = models.CharField(max_length=25)
    budget = models.FloatField()

    class Meta:
        verbose_name = ("Department")
        verbose_name_plural = ("Departments")

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("department_detail", kwargs={"pk": self.pk})