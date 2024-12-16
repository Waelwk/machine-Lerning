import pickle
import numpy as np

# Charger le modèle formé
try:
    with open('model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    print("Model loaded successfully")
    print(f"Model type: {type(model)}")
except Exception as e:
    print(f"Error loading model: {e}")

# Données de test
data = [17, 0, 5, 80, 70, 78, 90]
data_array = np.array(data).reshape(1, -1)
print(f"Data array: {data_array}")

try:
    prediction = model.predict(data_array)
    print(f"Prediction: {prediction}")
except Exception as e:
    print(f"Error during prediction: {e}")
