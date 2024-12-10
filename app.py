from flask import Flask, request, render_template
import joblib
import pandas as pd

app = Flask(__name__)

# Load the trained model
model = joblib.load('student_performance_model.joblib')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def predict():
    age = int(request.form['age'])
    gender = int(request.form['gender'])
    study_hours = int(request.form['study_hours'])
    courses_completed = int(request.form['courses_completed'])
    test_score = int(request.form['test_score'])
    reports_completed = int(request.form['reports_completed'])

    # Convert input values to a DataFrame
    input_data = pd.DataFrame({
        'Sexe': [gender],
        'Âge': [age],
        'Temps passé sur la plateforme (heures)': [study_hours],
        'Nombre de cours terminés (/10)': [courses_completed],
        'Résultat aux tests (/100)': [test_score],
        'Nombre de comptes rendus (/10)': [reports_completed]
    })

    # Predict the outcome
    prediction = model.predict(input_data)

    # Convert numerical prediction to categorical outcome
    outcome = 'Réussite' if prediction[0] == 1 else 'Échec'

    return render_template('index.html', outcome=outcome)

if __name__ == '__main__':
    app.run(debug=True)