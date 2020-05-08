from django.db import models
from .employee import Employee
from .training_program import TrainingProgram

class EmployeeTrainingProgram(models.Model):
    """
    Creates the join table for the many to many relationship between employees and training programs
    Author: Us
    methods: none
    """

    employee = models.ForeignKey("Employee", on_delete=models.CASCADE)
    training_program = models.ForeignKey("TrainingProgram", on_delete=models.CASCADE)
