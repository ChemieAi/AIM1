import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_predict
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix

# Load the dataset from the CSV file
dataset = pd.read_csv("dataset2.csv")

# Separate the features and labels
X = dataset.iloc[1:, 1:].values
y = dataset.iloc[1:, 0].values

# Perform standardization on the features
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Initialize classifiers
knn = KNeighborsClassifier()
svm = SVC()

# Define evaluation metrics
scoring = ['accuracy', 'precision_macro', 'recall_macro']

# Perform cross-validation and predict classes
knn_predictions = cross_val_predict(knn, X, y, cv=10)
svm_predictions = cross_val_predict(svm, X, y, cv=10)

# Compute evaluation metrics
knn_accuracy = accuracy_score(y, knn_predictions)
knn_precision = precision_score(y, knn_predictions, average='macro')
knn_recall = recall_score(y, knn_predictions, average='macro')

svm_accuracy = accuracy_score(y, svm_predictions)
svm_precision = precision_score(y, svm_predictions, average='macro')
svm_recall = recall_score(y, svm_predictions, average='macro')

# Fit kNN classifier using the entire dataset
knn.fit(X, y)

# Fit SVM classifier using the entire dataset
svm.fit(X, y)

# Compute confusion matrix for kNN classifier
knn_confusion_matrix = confusion_matrix(y, knn.predict(X))

# Compute confusion matrix for SVM classifier
svm_confusion_matrix = confusion_matrix(y, svm.predict(X))

# Print the evaluation results
print("kNN Accuracy:", knn_accuracy)
print("kNN Precision:", knn_precision)
print("kNN Recall:", knn_recall)
print("\n")
print("SVM Accuracy:", svm_accuracy)
print("SVM Precision:", svm_precision)
print("SVM Recall:", svm_recall)
print("\n")
print("kNN Confusion Matrix:")
print(knn_confusion_matrix)
print("\n")
print("SVM Confusion Matrix:")
print(svm_confusion_matrix)

# User enters a new sample
new_sample = [5, 6, 3, 8, 2, 4, 1, 10, 6, 9, 8, 5, 3, 1, 7, 4, 2, 10, 6, 9, 8]

# Perform standardization on the new sample
new_sample = scaler.transform([new_sample])

# Predict the class of the new sample using kNN classifier
knn_predicted_class = knn.predict(new_sample)
print("\n")
print("kNN Predicted Class:", knn_predicted_class)

# Predict the class of the new sample using SVM classifier
svm_predicted_class = svm.predict(new_sample)
print("SVM Predicted Class:", svm_predicted_class)
