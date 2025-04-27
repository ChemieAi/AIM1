import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings("ignore")
# gereken kutuphaneler import edildi

df = pd.read_csv('mushrooms.csv', delimiter=',')
'''https://www.kaggle.com/uciml/mushroom-classification'''

# df.head(5)

df.columns

df['class'].value_counts()

import matplotlib.pyplot as plt

plt.figure(figsize=(6, 6))
plt.pie(x=df['class'].value_counts(), explode=[0, 0.05], autopct='%0.01f%%', labels=['Edible', 'Poisonous'])
plt.title("Distribution of 'Class' column")
plt.show()
# hedef oznoiteligin piechart dagilimi
# buun veri setinde bias olup olmadigini gormek ici yaptik


from sklearn.preprocessing import LabelEncoder


def label_encoded(feature):
    le = LabelEncoder()
    le.fit(feature)
    print(feature.name, le.classes_)
    return le.transform(feature)


for col in df.columns:
    df[str(col)] = label_encoded(df[str(col)])

import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 10))
ax = sns.heatmap(df.corr())

df_corr = df.drop(['bruises', 'gill-spacing', 'gill-color', 'stalk-root', 'ring-type'], axis=1)

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    df_corr.drop(['class'], axis=1),
    df_corr['class'], test_size=0.33, random_state=42)

from sklearn.neighbors import KNeighborsClassifier

neigh = KNeighborsClassifier(weights='distance', n_jobs=-1, n_neighbors=11)
neigh.fit(X_train, y_train)

from sklearn.metrics import accuracy_score

y_pred = neigh.predict(X_test)
accuracy_score(y_test, y_pred)

import matplotlib.pyplot as plt
from sklearn.metrics import plot_confusion_matrix
from sklearn.model_selection import train_test_split

plot_confusion_matrix(neigh, X_test, y_test)

print("Enter the features for the new mushroom: (use one comma between features) ")
print('cap-shape', 'cap-surface', 'cap-color', 'odor', 'gill-attachment', 'gill-size', 'stalk-shape',
      'stalk-surface-above-ring', 'stalk-surface-below-ring', 'stalk-color-above-ring', 'stalk-color-below-ring',
      'veil-type', 'veil-color', 'ring-number', 'spore-print-color', 'population', 'habitat')
#### Example for your ease of use 3,2,8,3,0,1,1,2,2,7,7,0,2,1,3,2,3
value = input().split(',')
gues = neigh.predict([value])
for i in value:
    i = int(i)
print()
print("Prediction is ", gues[0])

from sklearn.svm import SVC

model = SVC(gamma=0.001)
model.fit(X_train, y_train)

plot_confusion_matrix(model, X_test, y_test)

y_pred_svc = model.predict(X_test)
accuracy_score(y_test, y_pred_svc)

print("Enter the features for the new mushroom: (use one comma between features) ")
print('cap-shape', 'cap-surface', 'cap-color', 'odor', 'gill-attachment', 'gill-size', 'stalk-shape',
      'stalk-surface-above-ring', 'stalk-surface-below-ring', 'stalk-color-above-ring', 'stalk-color-below-ring',
      'veil-type', 'veil-color', 'ring-number', 'spore-print-color', 'population', 'habitat')
#### Example for your ease of use 3,2,8,3,0,1,1,2,2,7,7,0,2,1,3,2,3
value = input().split(',')
gues = model.predict([value])
for i in value:
    i = int(i)
print()
print("Prediction is ", gues[0])

import matplotlib.pyplot as plt
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.model_selection import learning_curve
from sklearn.model_selection import ShuffleSplit


def plot_learning_curve(estimator, title, X, y, axes=None, ylim=None, cv=None,
                        n_jobs=None, train_sizes=np.linspace(.1, 1.0, 5)):
    """
    Generate 3 plots: the test and training learning curve, the training
    samples vs fit times curve, the fit times vs score curve.
    """
    if axes is None:
        _, axes = plt.subplots(1, 3, figsize=(20, 5))

    axes[0].set_title(title)
    if ylim is not None:
        axes[0].set_ylim(*ylim)
    axes[0].set_xlabel("Training examples")
    axes[0].set_ylabel("Score")

    train_sizes, train_scores, test_scores, fit_times, _ = \
        learning_curve(estimator, X, y, cv=cv, n_jobs=n_jobs,
                       train_sizes=train_sizes,
                       return_times=True)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    fit_times_mean = np.mean(fit_times, axis=1)
    fit_times_std = np.std(fit_times, axis=1)

    # Plot learning curve
    axes[0].grid()
    axes[0].fill_between(train_sizes, train_scores_mean - train_scores_std,
                         train_scores_mean + train_scores_std, alpha=0.1,
                         color="r")
    axes[0].fill_between(train_sizes, test_scores_mean - test_scores_std,
                         test_scores_mean + test_scores_std, alpha=0.1,
                         color="g")
    axes[0].plot(train_sizes, train_scores_mean, 'o-', color="r",
                 label="Training score")
    axes[0].plot(train_sizes, test_scores_mean, 'o-', color="g",
                 label="Cross-validation score")
    axes[0].legend(loc="best")

    # Plot n_samples vs fit_times
    axes[1].grid()
    axes[1].plot(train_sizes, fit_times_mean, 'o-')
    axes[1].fill_between(train_sizes, fit_times_mean - fit_times_std,
                         fit_times_mean + fit_times_std, alpha=0.1)
    axes[1].set_xlabel("Training examples")
    axes[1].set_ylabel("fit_times")
    axes[1].set_title("Scalability of the model")

    # Plot fit_time vs score
    axes[2].grid()
    axes[2].plot(fit_times_mean, test_scores_mean, 'o-')
    axes[2].fill_between(fit_times_mean, test_scores_mean - test_scores_std,
                         test_scores_mean + test_scores_std, alpha=0.1)
    axes[2].set_xlabel("fit_times")
    axes[2].set_ylabel("Score")
    axes[2].set_title("Performance of the model")

    return plt


fig, axes = plt.subplots(3, 2, figsize=(10, 15))

title = "Learning Curves, Knn"
# Cross validation with 100 iterations to get smoother mean test and train
# score curves, each time with 20% data randomly selected as a validation set.
cv = ShuffleSplit(n_splits=100, test_size=0.2, random_state=0)

estimator = KNeighborsClassifier()
plot_learning_curve(estimator, title, X_train, y_train, axes=axes[:, 0], ylim=(0.7, 1.01),
                    cv=cv, n_jobs=-1)

title = r"Learning Curves (SVC, RBF kernel, $\gamma=0.001$)"
# SVC is more expensive so we do a lower number of CV iterations:
cv = ShuffleSplit(n_splits=10, test_size=0.2, random_state=0)
estimator = SVC(gamma=0.001)
plot_learning_curve(estimator, title, X_train, y_train, axes=axes[:, 1], ylim=(0.7, 1.01),
                    cv=cv, n_jobs=-1)

plt.show()

from sklearn.ensemble import RandomForestClassifier

feature_names = [f'feature {i}' for i in range(X_train.shape[1])]
forest = RandomForestClassifier(random_state=0, n_jobs=-1, )
forest.fit(X_train, y_train)

import time
import numpy as np

start_time = time.time()
importances = forest.feature_importances_
std = np.std([
    tree.feature_importances_ for tree in forest.estimators_], axis=0)
elapsed_time = time.time() - start_time

print(f"Elapsed time to compute the importances: "
      f"{elapsed_time:.3f} seconds")

import pandas as pd

forest_importances = pd.Series(importances, index=feature_names)

fig, ax = plt.subplots()
forest_importances.plot.bar(yerr=std, ax=ax)
ax.set_title("Feature importances using MDI")
ax.set_ylabel("Mean decrease in impurity")
fig.tight_layout()
