import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from hrapp.models import model_factory, Computer, Employee
from ..connection import Connection


def get_assigned_employee(computer_id):
    with sqlite3.connect(Connection.db_path) as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
            SELECT
                e.first_name,
                e.last_name,
                d.name,
                ec.assign_date
            FROM hrapp_employeecomputer AS ec 
            JOIN hrapp_employee AS e ON ec.employee_id = e.id
            JOIN hrapp_department AS d ON e.department_id = d.id
            WHERE ec.computer_id = ?
        """, (computer_id,))

        response = db_cursor.fetchone()
        
        if response:
            employee = Employee()
            employee.first_name = response[0]
            employee.last_name = response[1]
            employee.department_name = response[2]
            employee.assigned_computer_date = response[3]
            return employee
        else:
            return None

def get_computer(computer_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Computer)
        db_cursor = conn.cursor()

        db_cursor.execute("""
            SELECT
                c.id,
                c.make,
                c.manufacturer,
                c.purchase_date,
                c.decommission_date
            FROM hrapp_computer AS c
            WHERE c.id = ?
        """, (computer_id,))

        return db_cursor.fetchone()


def computer_details(request, computer_id):
    if request.method == 'GET':
        computer = get_computer(computer_id)

        assigned_employee = get_assigned_employee(computer_id)

        template = 'computers/detail.html'
        context = {
            'computer': computer,
            'assigned_employee': assigned_employee
        }

        return render(request, template, context)
    
