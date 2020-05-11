from django.db import models
from django.urls import reverse
from .employee import Employee

class Computer(models.Model):
    '''
    description: This class creates a computer and its properties
    author: Joe Shep
    properties:
      make: The make will contain the name of the brand of the computer.
      purchase_date: This property contains the purchase date in string form.
      decomission_date: This property contains the dicomission date in string form.
      employees: This property contains the many to many relationship with the computer/employee model
    '''

    make = models.CharField(max_length=25)
    manufacturer = models.CharField(max_length=25)
    purchase_date = models.DateField()
    decommission_date = models.DateField(null=True, blank=True, default=None)
    employees = models.ManyToManyField("Employee", through='EmployeeComputer', default=None)

    class Meta:
        verbose_name = ("Computer")
        verbose_name_plural = ("Computers")

    def get_absolute_url(self):
        return reverse("computer_detail", kwargs={"pk": self.pk})