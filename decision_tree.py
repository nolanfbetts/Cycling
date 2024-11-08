import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import tree, ensemble
from sklearn.model_selection import cross_val_score
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import KFold
from collections import defaultdict
import pprint

data = pd.read_csv('./data/CompleteDataSetMVC.csv')


RANDOM_STATE = 10
FIGSIZE = (12,8)

crash_data = data

potential_features = [
    'NUMBER OF PERSONS INJURED', 'NUMBER OF PEDESTRIANS INJURED',
    'NUMBER OF CYCLIST INJURED', 'NUMBER OF MOTORIST INJURED'
]

max_depths, scores, cv_scores = range(1,11), [], []
dtcs = []
for max_depth in max_depths:
    dtc = tree.DecisionTreeClassifier(max_depth=max_depth, random_state=RANDOM_STATE)
    dtc.fit(crash_data[potential_features], crash_data['NUMBER OF CYCLIST INJURED'])
    score = dtc.score(crash_data[potential_features], crash_data['NUMBER OF CYCLIST INJURED'])
    scores.append(score)
    dtcs.append(dtc)
    dtc = tree.DecisionTreeClassifier(max_depth=max_depth, random_state=RANDOM_STATE)
    cv = KFold(n_splits=10, shuffle=True, random_state=RANDOM_STATE)
    cv_score = cross_val_score(dtc, crash_data[potential_features], crash_data['NUMBER OF CYCLIST INJURED'], cv=cv).mean()
    cv_scores.append(cv_score)


best_score_indices = np.where(scores == max(scores))[0]
best_depths = [max_depths[i] for i in best_score_indices]
print("Best depth settings when using the full dataset: ", best_depths)
plt.figure(figsize=FIGSIZE)
tree.plot_tree(dtcs[4])
best_cv_score_indices = np.where(cv_scores == max(cv_scores))[0]
best_cv_score_depths = [max_depths[i] for i in best_cv_score_indices]
print("Best depth settings when using cross-validation: ", best_cv_score_depths)


plt.figure(figsize=FIGSIZE)
plt.plot(max_depths, scores, label='Full Dataset')
plt.plot(max_depths, cv_scores, label='Cross-Validation')
plt.xlabel('Max Depth')
plt.ylabel('Accuracy')
plt.title('Decision Tree Classifier: Accuracy vs Max Depth')
plt.legend()
plt.show()
    