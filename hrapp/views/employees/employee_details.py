import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from hrapp.models import Employee
from ..connection import Connection


def get_employee(employee_id):
    with sqlite3.connect(Connection.db_path) as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.first_name,
            e.last_name,
            e.start_date,
            e.is_supervisor,
            d.id,
            d.name
        FROM hrapp_employee AS e
        JOIN hrapp_department AS d ON e.department_id = d.Id
        WHERE e.id = ?
        """, (employee_id,))

        response = db_cursor.fetchone()
        print(response)
        employee = Employee()
        employee.first_name = response[0]
        employee.last_name = response[1]
        employee.start_date = response[2]
        employee.is_supervisor = response[3]
        employee.department_name = response[5]

        return employee

# @login_required
def employee_details(request, employee_id):
    if request.method == 'GET':
        employee = get_employee(employee_id)
        template = 'employees/employee_details.html'
        context = {
            'employee': employee
        }

        return render(request, template, context)
    
    elif request.method == 'POST':
            
        form_data = request.POST

        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "PUT"
        ):   
            with sqlite3.connect(Connection.db_path) as conn:
                    db_cursor = conn.cursor()
                    db_cursor.execute("""
                    UPDATE hrapp_employee
                    SET first_name = ?,
                        last_name = ?,
                        start_date = ?,
                        is_supervisor = ?,
                        department_id = ?
                    WHERE id = ?
                    """,
                    (
                        form_data['first_name'], form_data['last_name'],  form_data['start_date'],
                        form_data['is_supervisor'], form_data['department_id'],
                    ))
            return redirect(reverse('hrapp:employee_list'))
            
        # if(
        #     "actual_method" in form_data
        #     and form_data["actual_method"] == "DELETE"
        # ):
        #     with sqlite3.connect(Connection.db_path) as conn:
        #         db_cursor = conn.cursor()

        #         db_cursor.execute("""
        #         DELETE FROM hrapp_employee
        #         WHERE id = ?
        #         """, (employee_id,))

        #     return redirect(reverse('hrapp:employee_list'))