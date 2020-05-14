import sqlite3
from django.shortcuts import render
from hrapp.models import Computer, Employee
from ..connection import Connection


def computer_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
            SELECT
                c.id,
                c.make,
                c.manufacturer,
                c.purchase_date,
                c.decommission_date,
                ec.assign_date
            FROM hrapp_computer AS c
            LEFT JOIN hrapp_employeecomputer AS ec ON c.id = ec.computer_id
            ORDER BY c.manufacturer
            """)

            all_computers = []
            dataset = db_cursor.fetchall()

            for i, row in enumerate(dataset):
                computer = Computer()
                computer.id = row['id']
                computer.make = row['make']
                computer.manufacturer = row['manufacturer']
                computer.purchase_date = row['purchase_date']
                computer.decommission_date = row['decommission_date']
                computer.is_assigned = row['assign_date']
                all_computers.append(computer)

            db_cursor.execute("""
        SELECT
            e.id,
            e.first_name,
            e.last_name,
            e.department_id,
            d.name,
            ec.assign_date
        FROM hrapp_employee AS e
        JOIN hrapp_department AS d ON e.department_id = d.id
        LEFT JOIN hrapp_employeecomputer AS ec ON ec.employee_id = e.id
        WHERE ec.employee_id IS NULL
        """)

        all_employees = []
        dataset = db_cursor.fetchall()
        print(len(dataset))
        for row in dataset:
            employee = Employee()
            employee.id = row['id']
            employee.first_name = row['first_name']
            employee.last_name = row['last_name']
            employee.department_name = row['name']
            all_employees.append(employee)

        template = 'computers/list.html'
        context = {
            'all_computers': all_computers,
            'employees': all_employees
        }

        return render(request, template, context)
    
    elif request.method == 'POST':
        form_data = request.POST
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
            select
                c.id,
                c.make,
                c.manufacturer,
                c.purchase_date,
                c.decommission_date
            from hrapp_computer c
            """)

            all_computers = []
            dataset = db_cursor.fetchall()

            for row in dataset:
                computer = Computer()
                computer.id = row['id']
                computer.make = row['make']
                computer.manufacturer = row['manufacturer']
                computer.purchase_date = row['purchase_date']
                computer.decommission_date = row['decommission_date']
                if computer.make.upper() == form_data['searchfield'].upper() or computer.manufacturer.upper() == form_data['searchfield'].upper():
                    all_computers.append(computer)
                elif form_data['searchfield'] == "":
                    all_computers.append(computer)

        template = 'computers/list.html'
        context = {
            'all_computers': all_computers
        }

        return render(request, template, context)