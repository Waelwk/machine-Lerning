from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base

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
    attempt_number = Column(Integer, default=1)  # Ajoutez ici le nombre d'essais, par exemple par défaut 1


DATABASE_URI = 'mysql+mysqlconnector://root:root@localhost:8889/students_db'
engine = create_engine(DATABASE_URI)
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Ajouter quelques exemples d'étudiants
student1 = Student(name="Alice", age=17, gender=0, study_hours=5, assignment_grade=80, test_score=70, quiz_score=78, final_project_grade=90)
student2 = Student(name="Bob", age=18, gender=1, study_hours=6, assignment_grade=85, test_score=75, quiz_score=88, final_project_grade=92)
student3 = Student(name="Charlie", age=16, gender=1, study_hours=7, assignment_grade=75, test_score=65, quiz_score=70, final_project_grade=80)
student4 = Student(name="Daisy", age=17, gender=0, study_hours=8, assignment_grade=90, test_score=95, quiz_score=90, final_project_grade=95)
student5 = Student(name="Eve", age=18, gender=0, study_hours=4, assignment_grade=60, test_score=55, quiz_score=60, final_project_grade=70)

# Ajouter les nouveaux exemples
student6 = Student(age=16, gender=0, study_hours=2, assignment_grade=62, test_score=46, quiz_score=49, final_project_grade=61)
student7 = Student(age=17, gender=1, study_hours=3, assignment_grade=64, test_score=52, quiz_score=51, final_project_grade=67)
student8 = Student(age=18, gender=0, study_hours=2, assignment_grade=58, test_score=42, quiz_score=47, final_project_grade=59)
student9 = Student(age=16, gender=1, study_hours=1, assignment_grade=60, test_score=48, quiz_score=53, final_project_grade=65)

session.add(student1)
session.add(student2)
session.add(student3)
session.add(student4)
session.add(student5)
session.add(student6)
session.add(student7)
session.add(student8)
session.add(student9)
session.commit()

# Afficher les étudiants pour vérifier qu'ils ont été ajoutés
students = session.query(Student).all()
for student in students:
    print(f"ID: {student.id}, Name: {student.name}, Age: {student.age}, Gender: {student.gender}, Study Hours: {student.study_hours}, Assignment Grade: {student.assignment_grade}, Test Score: {student.test_score}, Quiz Score: {student.quiz_score}, Final Project Grade: {student.final_project_grade}")
