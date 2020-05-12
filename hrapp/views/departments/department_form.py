import sqlite3
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from hrapp.models import Department
from ..connection import Connection


# @login_required
def department_form(request):
    if request.method == 'GET':
        template = 'departments/department_form.html'

        return render(request, template)
    
    elif request.method == 'POST':
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO hrapp_department
            (
                name, budget
            )
            VALUES (?, ?)
            """,
            (form_data['name'], form_data['budget']))

        return redirect(reverse('hrapp:department_list'))