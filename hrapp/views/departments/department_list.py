import sqlite3
from django.shortcuts import render
from hrapp.models import Department
from ..connection import Connection


def department_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # TODO: Add to query: e.department,
            db_cursor.execute("""
            SELECT
                d.id,
                d.name,
                d.budget
            FROM hrapp_department AS d
            ORDER BY d.name
            """)

            all_departments = []
            dataset = db_cursor.fetchall()

            for row in dataset:
                department = Department()
                department.id = row['id']
                department.name = row['name']
                department.budget = row['budget']

                all_departments.append(department)

    template = 'departments/department_list.html'
    context = {
        'departments': all_departments
    }

    return render(request, template, context)
