from flask import Flask, request, jsonify, render_template, redirect, url_for
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)

# Configuration de la base de données
DATABASE_URI = 'mysql+mysqlconnector://root:root@localhost:8889/students_db'
engine = create_engine(DATABASE_URI)
Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    age = Column(Integer)
    gender = Column(Integer)  # 0 pour féminin, 1 pour masculin
    study_hours = Column(Float)
    assignment_grade = Column(Float)
    test_score = Column(Float)
    quiz_score = Column(Float)
    final_project_grade = Column(Float)

Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Charger le modèle formé
try:
    with open('model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    print("Model loaded successfully")
except Exception as e:
    print(f"Error loading model: {e}")

@app.route('/')
def home():
    try:
        students = session.query(Student).all()
        return render_template('index.html', students=students)
    except Exception as e:
        return f"Error loading students: {e}"

@app.route('/predict/<int:student_id>', methods=['GET'])
def predict(student_id):
    try:
        student = session.query(Student).filter_by(id=student_id).one()
        
        # Ensure features are ordered exactly the same as in the model
        data = [
            student.age,
            student.gender,
            student.study_hours,
            student.assignment_grade,
            student.test_score,
            student.quiz_score,
            student.final_project_grade
        ]
        
        # Check if the data is in the correct shape for the model
        data_array = np.array(data).reshape(1, -1)
        
        # Predict and map result
        prediction = model.predict(data_array)
        prediction_int = int(prediction[0])
        result = "Réussi" if prediction_int == 1 else "Échoué"
        
        return jsonify({'prediction': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/add', methods=['POST'])
def add_student():
    try:
        student_data = request.form
        new_student = Student(
            name=student_data['name'],
            age=int(student_data['age']),
            gender=int(student_data['gender']),
            study_hours=float(student_data['study_hours']),
            assignment_grade=float(student_data['assignment_grade']),
            test_score=float(student_data['test_score']),
            quiz_score=float(student_data['quiz_score']),
            final_project_grade=float(student_data['final_project_grade'])
        )
        session.add(new_student)
        session.commit()
        return redirect(url_for('home'))
    except Exception as e:
        return f"Error adding student: {e}"

@app.route('/update/<int:student_id>', methods=['POST'])
def update_student(student_id):
    try:
        student = session.query(Student).filter_by(id=student_id).one()
        student_data = request.form
        student.name = student_data['name']
        student.age = int(student_data['age'])
        student.gender = int(student_data['gender'])
        student.study_hours = float(student_data['study_hours'])
        student.assignment_grade = float(student_data['assignment_grade'])
        student.test_score = float(student_data['test_score'])
        student.quiz_score = float(student_data['quiz_score'])
        student.final_project_grade = float(student_data['final_project_grade'])
        session.commit()
        return redirect(url_for('home'))
    except Exception as e:
        return f"Error updating student: {e}"

@app.route('/delete/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    try:
        student = session.query(Student).filter_by(id=student_id).one()
        session.delete(student)
        session.commit()
        return redirect(url_for('home'))
    except Exception as e:
        return f"Error deleting student: {e}"

if __name__ == '__main__':
    app.run(debug=True)
