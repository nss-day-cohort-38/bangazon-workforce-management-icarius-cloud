import sqlite3
from hrapp.views.training_programs.detail import get_training_program
from django.shortcuts import render, redirect, reverse

def training_program_form(request):
    if request.method == 'GET':
        template = 'training_programs/training_program_form.html'
        context = {}
        return render(request, template, context)
    
def training_program_edit_form(request, training_program_id):
    if request.method == 'GET':
        training_program = get_training_program(training_program_id)
        template = 'training_programs/training_program_form.html'
        context = {
            'training_program': training_program
        }
        return render(request, template, context)