from flask import Flask, request, jsonify, render_template, redirect, url_for
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm.exc import NoResultFound
import numpy as np
import pickle

app = Flask(__name__)

# Configuration de la base de données
DATABASE_URI = 'mysql+mysqlconnector://root:root@localhost:8889/students_db'
engine = create_engine(DATABASE_URI)
Base = declarative_base()

# Modèle de la base de données
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
    attempt_number = Column(Integer)  # Nouvelle colonne

Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Charger le modèle formé
model = None
feature_columns = None
try:
    with open('trained_model.pkl', 'rb') as model_file:
        model, feature_columns = pickle.load(model_file)  # Charger modèle et colonnes
    print("Model loaded successfully")
except FileNotFoundError:
    print("Model file not found. Please ensure 'trained_model.pkl' exists.")
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
    if not model:
        return jsonify({'error': 'Model is not loaded. Please contact the administrator.'}), 500

    try:
        # Récupérer les données de l'étudiant dans la base
        student = session.query(Student).filter_by(id=student_id).one()

        # Préparer les données d'entrée
        data = {
            'Study Hours': student.study_hours,
            'Attempt Number': student.attempt_number,
            'Assignment Grade': student.assignment_grade,
            'Test Score': student.test_score,
            'Quiz Score': student.quiz_score
        }

        # Ordre des colonnes selon le modèle
        input_data = [data[col] for col in feature_columns]
        data_array = np.array(input_data).reshape(1, -1)

        # Faire une prédiction
        prediction = model.predict(data_array)
        result = "Réussi" if int(prediction[0]) == 1 else "Échoué"

        return jsonify({'prediction': result})

    except KeyError as e:
        return jsonify({'error': f'Missing feature: {str(e)}'}), 400
    except NoResultFound:
        return jsonify({'error': f'Student with id {student_id} not found.'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/add', methods=['POST'])
def add_student():
    try:
        # Validate that all required fields are provided
        required_fields = ['name', 'age', 'gender', 'study_hours', 'assignment_grade', 
                           'test_score', 'quiz_score', 'final_project_grade', 'attempt_number']
        for field in required_fields:
            if field not in request.form:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Parse and validate the inputs
        student_data = request.form
        new_student = Student(
            name=student_data['name'],
            age=int(student_data['age']),
            gender=int(student_data['gender']),
            study_hours=float(student_data['study_hours']),
            assignment_grade=float(student_data['assignment_grade']),
            test_score=float(student_data['test_score']),
            quiz_score=float(student_data['quiz_score']),
            final_project_grade=float(student_data['final_project_grade']),
            attempt_number=int(student_data['attempt_number'])
        )

        # Add the new student to the database
        session.add(new_student)
        session.commit()
        return redirect(url_for('home'))

    except ValueError as ve:
        return jsonify({'error': f'Invalid input type: {ve}'}), 400
    except Exception as e:
        return jsonify({'error': f'Error adding student: {str(e)}'}), 500

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
        student.attempt_number = int(student_data['attempt_number'])  # Mise à jour
        session.commit()
        return redirect(url_for('home'))
    except NoResultFound:
        return f"Student with id {student_id} not found."
    except Exception as e:
        return f"Error updating student: {e}"

@app.route('/delete/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    try:
        student = session.query(Student).filter_by(id=student_id).one()
        session.delete(student)
        session.commit()
        return redirect(url_for('home'))
    except NoResultFound:
        return f"Student with id {student_id} not found."
    except Exception as e:
        return f"Error deleting student: {e}"

if __name__ == '__main__':
    app.run(debug=True)
