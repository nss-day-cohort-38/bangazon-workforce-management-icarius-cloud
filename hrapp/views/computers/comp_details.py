import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from hrapp.models import model_factory, Computer
from ..connection import Connection


def get_computer(computer_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Computer)
        db_cursor = conn.cursor()

        db_cursor.execute("""
            select
                c.id,
                c.make,
                c.manufacturer,
                c.purchase_date,
                c.decommission_date
            from hrapp_computer c
            WHERE c.id = ?
        """, (computer_id,))

        return db_cursor.fetchone()


def computer_details(request, computer_id):
    if request.method == 'GET':
        computer = get_computer(computer_id)

        template = 'computers/detail.html'
        context = {
            'computer': computer
        }

        return render(request, template, context)