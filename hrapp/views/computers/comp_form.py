import sqlite3
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from hrapp.models import Computer
from ..connection import Connection


# @login_required
def computer_form(request):
    if request.method == 'GET':
        template = 'computers/form.html'

        return render(request, template)
    
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

        return redirect(reverse('hrapp:computers'))