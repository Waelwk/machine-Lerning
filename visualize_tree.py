# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.tree import DecisionTreeClassifier, plot_tree
# import matplotlib.pyplot as plt

# # Charger les données
# data = pd.read_csv('students.csv')

# # Sélectionner les features et la target
# features = ['Age', 'Gender', 'Study Hours', 'Assignment Grade', 'Test Score', 'Quiz Score', 'Final Project Grade', 'Attempt Number']
# target = 'Result'

# X = data[features]
# y = data[target]

# # Diviser les données en sets d'entraînement et de test
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Créer et entraîner le modèle
# model = DecisionTreeClassifier()
# model.fit(X_train, y_train)

# # Visualiser l'arbre de décision
# plt.figure(figsize=(20,10))
# plot_tree(model, feature_names=features, class_names=['Fail', 'Pass'], filled=True, rounded=True)
# plt.show()
