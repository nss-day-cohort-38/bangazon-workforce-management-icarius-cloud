import sqlite3
from django.shortcuts import render, redirect, reverse
from datetime import datetime
from hrapp.models import TrainingProgram
from ..connection import Connection


def training_program_list(request):
    if request.method == 'GET':
        # Connection.py holds db_path to specific db 
        with sqlite3.connect(Connection.db_path) as conn:
            # Row method makes into row factory 
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
            select
                tp.id,
                tp.title, 
                tp.start_date, 
                tp.end_date, 
                tp.capacity
            from hrapp_trainingprogram tp
            """)

            past_training_programs = []
            future_training_programs = []
            dataset = db_cursor.fetchall()

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
                   
               

        template = 'training_programs/training_program_list.html'

        context = {
            'past_training_programs': past_training_programs, 
            'future_training_programs': future_training_programs
        }
        return render(request, template, context)

    elif request.method == 'POST':
            form_data = request.POST
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                INSERT INTO hrapp_trainingprogram
                (
                    title, start_date, end_date, capacity
                )
                VALUES (?, ?, ?, ?)
                """,
                (form_data['title'], form_data['start_date'],
                    form_data['end_date'], form_data['capacity']))

            return redirect(reverse('hrapp:training_program_list'))


