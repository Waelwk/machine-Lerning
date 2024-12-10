import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
import joblib

df = pd.read_csv('Students_dataset.csv')

# Convert (Réussite = 1, Échec = 0)
df['Résultat'] = df['Résultat'].map({'Réussite': 1, 'Échec': 0})

df['Sexe'] = df['Sexe'].map({'Homme': 0, 'Femme': 1})

# Define features and target variable
X = df.drop(columns=['Résultat', 'ID Étudiant', 'Nom'])
y = df['Résultat']

# includ all features
print("Features used for training:")
print(df.drop(columns=['Résultat', 'ID Étudiant', 'Nom']).columns)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the decision tree model
model = DecisionTreeClassifier(random_state=42, max_depth=10, min_samples_split=2, min_samples_leaf=1)
model.fit(X_train, y_train)

# Save the trained model 
joblib.dump(model, 'student_performance_model.joblib')

# Test the model
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print(f'Accuracy: {accuracy}')
print('Classification Report:')
print(report)

# Perform stratified cross-validation
skf = StratifiedKFold(n_splits=5)
cv_scores = cross_val_score(model, X, y, cv=skf)

print(f'Stratified Cross-Validation Accuracy Scores: {cv_scores}')
print(f'Mean Stratified Cross-Validation Accuracy: {cv_scores.mean()}')

# Display feature importance
feature_importances = pd.Series(model.feature_importances_, index=df.drop(columns=['Résultat', 'ID Étudiant', 'Nom']).columns)
print('Feature Importances:')
print(feature_importances)


# Plot the decision tree
plt.figure(figsize=(30,20))
plot_tree(model, feature_names=df.drop(columns=['Résultat', 'ID Étudiant', 'Nom']).columns, class_names=['Échec', 'Réussite'], filled=True, rounded=True, fontsize=14, precision=2, proportion=True, impurity=False, label='root')
plt.savefig('decision_tree.png')
plt.show()