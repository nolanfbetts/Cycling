import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

data = pd.read_csv('./data/CompleteDataSetMVC.csv')

print(data.head())
# print(data.info())

# Example of selecting relevant columns
potential_features = [
    'NUMBER OF PERSONS INJURED', 'NUMBER OF PEDESTRIANS INJURED',
    'NUMBER OF CYCLIST INJURED', 'NUMBER OF MOTORIST INJURED'
]
target = 'NUMBER OF PERSONS KILLED'

# Drop rows with missing values in these columns
data = data.dropna(subset=potential_features + [target])

# Handle categorical data, e.g., one-hot encoding
data = pd.get_dummies(data, columns=['BOROUGH'], drop_first=True)
boroughs = ['BOROUGH_BROOKLYN', 'BOROUGH_MANHATTAN', 'BOROUGH_QUEENS', 'BOROUGH_STATEN ISLAND']
print(data.head())


# Extract hour from CRASH TIME if time is relevant
# data['CRASH_HOUR'] = pd.to_datetime(data['CRASH TIME']).dt.hour

# Prepare the feature matrix (X) and target vector (y)
X = data[potential_features + boroughs]
y = data[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Squared Error: {mse}')
print(f'R-squared: {r2}')