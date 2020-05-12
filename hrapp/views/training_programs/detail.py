import sqlite3
from django.urls import reverse
from hrapp.models import model_factory, TrainingProgram
from django.shortcuts import render, redirect
from ..connection import Connection

def get_training_program(training_program_id): 
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(TrainingProgram)
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            tp.id,
            tp.title, 
            tp.start_date, 
            tp.end_date, 
            tp.capacity
        FROM hrapp_trainingprogram tp
        WHERE tp.id = ?
        """, (training_program_id,))

        return db_cursor.fetchone()

def get_training_program_employees(training_program_id): 
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(TrainingProgram)
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
             etp.id, 
             etp.employee_id,
             etp.training_program_id, 
             e.id, 
             e.first_name, 
             e.last_name, 
             tp.id, 
             tp.title
             FROM hrapp_employeetrainingprogram AS etp
             JOIN hrapp_trainingprogram AS tp
             ON tp.id = etp.training_program_id
             JOIN hrapp_employee AS e
             ON e.id = etp.employee_id
             WHERE tp.id = ?    
        """, (training_program_id,))
        return db_cursor.fetchall()


def training_program_details(request, training_program_id):
    if(request.method == 'GET'):
        training_program = get_training_program(training_program_id)
        employees = get_training_program_employees(training_program_id)
        template = 'training_programs/training_program_detail.html'
        context = {
            'training_program': training_program, 
            'employees': employees
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
                    UPDATE hrapp_trainingprogram
                    SET title = ?,
                        start_date = ?,
                        end_date = ?,
                        capacity = ?
                    WHERE id = ?
                    """,
                    (
                        form_data['title'], form_data['start_date'],
                        form_data['end_date'], form_data['capacity'],
                        training_program_id,
                    ))
            return redirect(reverse('hrapp:training_program_list'))