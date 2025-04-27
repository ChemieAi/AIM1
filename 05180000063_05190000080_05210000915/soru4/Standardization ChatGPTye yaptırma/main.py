import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score

# Load dataset from CSV file (assuming it is separated by commas)
dataset = pd.read_csv("dataset2.csv", delimiter=",")

# Separate features and labels
features = dataset.iloc[:, :-1]
labels = dataset.iloc[:, -1]

# Standardize the dataset
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

# Train k-Nearest Neighbors (kNN) classifier with cross-validation
knn = KNeighborsClassifier()
knn_scores = cross_val_score(knn, features_scaled, labels, cv=10)

# Train Support Vector Machine (SVM) classifier with cross-validation
svm = SVC()
svm_scores = cross_val_score(svm, features_scaled, labels, cv=10)

# Print cross-validation scores
print("kNN Cross-Validation Scores:", knn_scores)
print("Mean kNN Cross-Validation Score:", np.mean(knn_scores))
print("SVM Cross-Validation Scores:", svm_scores)
print("Mean SVM Cross-Validation Score:", np.mean(svm_scores))

# Perform train-test split
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

# Standardize the dataset
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train k-Nearest Neighbors (kNN) classifier
knn.fit(X_train_scaled, y_train)

# Train Support Vector Machine (SVM) classifier
svm.fit(X_train_scaled, y_train)

# Ask user to enter a new sample
new_sample = np.array(input("Enter a new sample (22 features separated by spaces): ").split(), dtype=np.float64)
new_sample_scaled = scaler.transform(new_sample.reshape(1, -1))

# Predict using kNN classifier
new_sample_pred_knn = knn.predict(new_sample_scaled)

# Predict using SVM classifier
new_sample_pred_svm = svm.predict(new_sample_scaled)

# Compute confusion matrices
confusion_knn = confusion_matrix(y_test, knn.predict(X_test_scaled))
confusion_svm = confusion_matrix(y_test, svm.predict(X_test_scaled))

# Calculate evaluation metrics
accuracy_knn = accuracy_score(y_test, knn.predict(X_test_scaled))
accuracy_svm = accuracy_score(y_test, svm.predict(X_test_scaled))
precision_knn = precision_score(y_test, knn.predict(X_test_scaled), average='weighted')
precision_svm = precision_score(y_test, svm.predict(X_test_scaled), average='weighted')
recall_knn = recall_score(y_test, knn.predict(X_test_scaled), average='weighted')
recall_svm = recall_score(y_test, svm.predict(X_test_scaled), average='weighted')

# Print results
print("Confusion matrix (kNN):\n", confusion_knn)
print("Confusion matrix (SVM):\n", confusion_svm)
print("Accuracy (kNN):", accuracy_knn)
print("Accuracy (SVM):", accuracy_svm)
print("Precision (kNN):", precision_knn)
print("Precision (SVM):", precision_svm)
print("Recall (kNN):", recall_knn)
print("Recall (SVM):", recall_svm)
print("New sample:")
print(new_sample)
print("Class predicted by kNN classifier:", new_sample_pred_knn[0])
print("Class predicted by SVM classifier:", new_sample_pred_svm[0])
