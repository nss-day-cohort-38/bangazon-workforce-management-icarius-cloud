import sqlite3
from django.shortcuts import render, redirect, reverse
from datetime import datetime
from hrapp.models import TrainingProgram
from ..connection import Connection


def get_training_programs():
        with sqlite3.connect(Connection.db_path) as conn:
           
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
            SELECT
                tp.id,
                tp.title, 
                tp.start_date, 
                tp.end_date, 
                tp.capacity
            FROM hrapp_trainingprogram tp
            """)
            dataset = db_cursor.fetchall()
            past_training_programs = []
            future_training_programs = []
           

            for row in dataset:
                training_program = TrainingProgram()
                training_program.id = row["id"]
                training_program.title = row["title"]
                training_program.start_date = row["start_date"]
                training_program.end_date = row["end_date"]
                training_program.capacity = row["capacity"]
                if(datetime.strptime(training_program.start_date, "%Y-%m-%d") > datetime.now()):
                    future_training_programs.append(training_program)   
                else: 
                    past_training_programs.append(training_program)

            return future_training_programs


def assign_employee_form(request, employee_id):
    if request.method == 'GET':
        employee = request.GET.get('employee')
        
        programs = get_training_programs()
        with sqlite3.connect(Connection.db_path) as conn:
             
            conn.row_factory = sqlite3.Row
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
                    WHERE e.id = ?    
                """, (employee_id,))
        
        dataset = db_cursor.fetchall()
        context = {
            'programs': programs,
            'employee': employee_id
        }

        template = 'training_programs/assign_employee_form.html'
       
        return render(request, template, context)

    elif request.method == 'POST':
            form_data = request.POST
        
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                INSERT INTO hrapp_employeetrainingprogram
                (
                    employee_id, training_program_id
                )
                VALUES (?, ?)
                """,
                (form_data['hidden_employee'], form_data['training_program'],))
            # return redirect(reverse('hrapp:employee_details', args=[employee_id]))
            # Redirects based on kwargs or args that give the employee id
            return redirect(reverse('hrapp:employee_details', kwargs={'employee_id':employee_id}))