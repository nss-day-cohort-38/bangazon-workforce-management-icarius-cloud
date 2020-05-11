import sqlite3
from django.shortcuts import render, redirect, reverse

def training_program_form(request):
    if request.method == 'GET':
        template = 'training_programs/training_program_form.html'
        context = {}
        return render(request, template, context)