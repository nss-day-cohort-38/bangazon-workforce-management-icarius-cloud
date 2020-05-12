import sqlite3
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from hrapp.models import Computer, Employee, model_factory
from ..connection import Connection

def get_employees():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id,
            e.first_name,
            e.last_name,
            e.department_id,
            d.name
        FROM hrapp_employee AS e
        JOIN hrapp_department AS d
        ON e.department_id = d.id
        """)

        all_employees = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            employee = Employee()
            employee.id = row['id']
            employee.first_name = row['first_name']
            employee.last_name = row['last_name']
            employee.department_name = row['name']

            all_employees.append(employee)
        print(all_employees)
        return all_employees


# @login_required
def computer_form(request):
    if request.method == 'GET':
        employee_list = get_employees()
        template = 'computers/form.html'
        context = {
            'employees': employee_list
        }
        return render(request, template, context)
    
    elif request.method == 'POST':
        form_data = request.POST
        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO hrapp_computer
            (
                manufacturer, make, purchase_date
            )
            VALUES (?, ?, ?)
            """,
            (form_data['manufacturer'], form_data['make'], form_data['purchase_date']))

            if hasattr(form_data,'employee'):

                db_cursor.execute("""
                INSERT INTO hrapp_employeecomputer
                (assign_date, unassigned_date, computer_id, employee_id)
                VALUES (?, ?, ?, ?)
                """,
                (form_data['purchase_date'], "N/A", db_cursor.lastrowid, form_data['employee']))

            

        return redirect(reverse('hrapp:computers'))