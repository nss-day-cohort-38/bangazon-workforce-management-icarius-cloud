import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from hrapp.models import Department, Employee
from ..connection import Connection


def get_department(department_name):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            d.name,
            d.budget,
            e.first_name,
            e.last_name,
            e.is_supervisor
        FROM hrapp_department AS d
        LEFT JOIN hrapp_employee AS e ON e.department_id = d.id
        WHERE d.name = ?
        """, (department_name,))

        response = db_cursor.fetchall()
        print("***SDFVSER***", response)
        for row in response:
            if row == response[0]:
                department = Department()
                department.employees = []
                department.name = row['name']
                department.budget = row['budget']
                employee = Employee()
                employee.first_name = row['first_name']
                employee.last_name = row['last_name']
                employee.is_supervisor = row['is_supervisor']
                department.employees.append(employee)
            else:
                employee = Employee()
                employee.first_name = row['first_name']
                employee.last_name = row['last_name']
                employee.is_supervisor = row['is_supervisor']
                department.employees.append(employee)
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