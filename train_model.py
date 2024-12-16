import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.tree import export_text, plot_tree
import matplotlib.pyplot as plt
import joblib
import pickle

# Charger le dataset
df = pd.read_csv('students.csv')  # Remplacez par le chemin de votre fichier CSV

# Vérifier les premières lignes pour comprendre les données
print(df.head())

# Vérifier la répartition des classes
print(df['Result'].value_counts())

# Réorganiser les colonnes selon l'ordre souhaité
X = df[['Study Hours', 'Attempt Number', 'Assignment Grade', 'Test Score', 'Quiz Score']]  # Colonnes dans l'ordre souhaité
y = df['Result']  # Colonne cible (échec ou réussite)

# Diviser les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Créer le modèle d'arbre de décision avec un ajustement de profondeur
clf = DecisionTreeClassifier(
    criterion='entropy',
    max_depth=10,  # Profondeur plus grande pour capturer plus de relations
    min_samples_split=2,
    min_samples_leaf=1,
    random_state=42
)

# Entraîner le modèle
clf.fit(X_train, y_train)

# Prédire les résultats sur l'ensemble de test
y_pred = clf.predict(X_test)

# Calculer l'accuracy
print("Accuracy:", accuracy_score(y_test, y_pred))

# Afficher le rapport de classification
print("\nRapport de classification :\n", classification_report(y_test, y_pred))

# Sauvegarder le modèle entraîné avec joblib
joblib.dump(clf, 'trained_model.pkl')

# Sauvegarder le modèle entraîné avec pickle
with open('trained_model.pkl', 'wb') as model_file:
    pickle.dump(clf, model_file)

print("Modèle sauvegardé avec succès sous le nom 'trained_model.pkl'")

# Afficher les règles textuelles de l'arbre de décision
print("\nArbre de Décision - Règles Textuelles :\n", export_text(clf, feature_names=list(X.columns)))

# Visualiser l'arbre de décision
plt.figure(figsize=(20,10))  # Ajuster la taille de la figure pour mieux voir l'arbre
plot_tree(
    clf,
    filled=True,                    # Remplir les nœuds avec des couleurs
    feature_names=X.columns,        # Afficher les noms des caractéristiques
    class_names=['Échec', 'Réussite'],  # Nom des classes
    rounded=True,                   # Coins arrondis
    proportion=True,                # Proportion des classes dans chaque nœud
    precision=2,                    # Précision des valeurs numériques affichées
    fontsize=12                     # Taille de la police
)

plt.title("Arbre de Décision - Prédiction des Résultats", fontsize=16)  # Ajouter un titre à l'arbre
plt.show()
# Save the model along with its feature columns
with open('trained_model.pkl', 'wb') as model_file:
    pickle.dump((clf, list(X.columns)), model_file)

print("Model and feature names saved successfully as 'trained_model.pkl'")
