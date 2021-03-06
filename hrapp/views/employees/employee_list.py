import sqlite3
from django.shortcuts import render, redirect, reverse
from hrapp.models import Employee, Department
from ..connection import Connection
from django.contrib.auth.decorators import login_required

def employee_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
           SELECT
                e.id,
                e.first_name,
                e.last_name,
                e.start_date,
                e.is_supervisor,
                d.name
            FROM hrapp_employee e
            JOIN hrapp_department d               
            ON e.department_id = d.id
            ORDER BY e.first_name
            """)

            all_employees = []
            dataset = db_cursor.fetchall()

            for row in dataset:
                employee = Employee()
                employee.id = row['id']
                employee.first_name = row['first_name']
                employee.last_name = row['last_name']
                employee.start_date = row['start_date']
                employee.is_supervisor = row['is_supervisor']
                employee.department_name = row['name']

                all_employees.append(employee)
                
                db_cursor.execute("""
                select
                    d.id,
                    d.name
                from hrapp_department d
                """)

                all_departments = db_cursor.fetchall()
                
        template = 'employees/employees_list.html'
        context = {
            'employees': all_employees,
            'all_departments': all_departments
        }

        return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO hrapp_employee
            (
                first_name, last_name, start_date, is_supervisor,
                department_id
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (form_data['first_name'], form_data['last_name'],
                form_data['start_date'], form_data['is_supervisor'], form_data['department_id']))

        return redirect(reverse('hrapp:employee_list'))