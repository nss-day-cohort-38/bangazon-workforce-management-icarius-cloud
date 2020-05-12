import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from hrapp.models import Department
from ..connection import Connection


def get_department(department_name):
    with sqlite3.connect(Connection.db_path) as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            d.name,
            d.budget
        FROM hrapp_department AS d
        WHERE d.name = ?
        """, (department_name,))

        response = db_cursor.fetchone()
        department = Department()
        department.name = response[0]
        department.budget = response[1]

        return department

# @login_required
def department_details(request, department_name):
    if request.method == 'GET':
        department = get_department(department_name)
        template = 'departments/department_details.html'
        context = {
            'department': department
        }

        return render(request, template, context)