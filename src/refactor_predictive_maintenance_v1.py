import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.metrics import classification_report
from sklearn.model_selection import cross_val_score

# Loading and exploring the data
def load_data(filepath):
    data = pd.read_csv(filepath)
    return data

def explore_data(data):
    print(data.head().T)
    print(data.describe())
    print(data.info())

# Visualizing the data
# Define a function to create histograms and boxplots for numerical columns
def plot_numerical_columns(df, numerical_columns):

    # Set the style for seaborn plots
    sns.set_style("whitegrid")
    # Calculating the number of rows needed for the subplots
    n_columns = 4
    n_rows = int(len(numerical_columns) * 2 / n_columns)
    
    if len(numerical_columns) * 2 % n_columns != 0:
        n_rows += 1

    # Create subplots
    fig, axs = plt.subplots(n_rows, n_columns, figsize=(17, 3 * n_rows))

    for i, column in enumerate(numerical_columns):
        row = (i * 2) // n_columns
        col = (i * 2) % n_columns

        # Histogram
        sns.histplot(df[column], bins=30, ax=axs[row, col], kde=True)
        axs[row, col].set_title(f'Histogram of {column}')

        # Boxplot
        sns.boxplot(x=df[column], ax=axs[row, col + 1])
        axs[row, col + 1].set_title(f'Boxplot of {column}')

    plt.tight_layout()
    plt.show()

def plot_correlation_matrix(data, numerical_columns):
    plt.figure(figsize=(12, 8))
    sns.heatmap(data[numerical_columns].corr(), annot=True, fmt=".2f", cmap='coolwarm')
    plt.show()

# Preprocessing and feature engineering
def intermediate_data(data, columns_to_drop):
    return data.drop(columns_to_drop, axis=1)

def scale_features(data, target):
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(data.drop(target, axis=1))
    data_scaled = pd.DataFrame(features_scaled, columns=data.columns[:-1])
    data_scaled[target] = data[target]
    return data_scaled

# Splitting the dataset
def split_data(data, target, test_size=0.2, random_state=42):
    X = data.drop(target, axis=1)
    y = data[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    return X_train, X_test, y_train, y_test

# Training the model
def train_model(X_train, y_train):
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    return model

# Evaluating the model
def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    print("Confusion Matrix:")
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.show()
    
    report = classification_report(y_test, y_pred)
    print("Classification Report:")
    print(report)

# Validación cruzada
def cross_validate_model(model, X, y, cv=5):
    scores = cross_val_score(model, X, y, cv=cv)
    print("Average accuracy with CV:", np.mean(scores))

# Main function to run the pipeline
# Main function for running the pipeline
def main(filepath):
    print(filepath)
    data = load_data(filepath)
    print(data)
    numerical_columns = data.select_dtypes(include = ['int', 'float']).columns
    explore_data(data)
    plot_numerical_columns(data, numerical_columns)
    plot_correlation_matrix(data, numerical_columns)
    interim_df = intermediate_data(data, ["Product ID", "Type"])
    data_scaled = scale_features(interim_df, 'Machine failure')
    X_train, X_test, y_train, y_test = split_data(data_scaled, 'Machine failure')
    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)
    cross_validate_model(model, data_scaled.drop('Machine failure', axis=1), data_scaled['Machine failure'])

if __name__ == '__main__':
    main(filepath=r'D:\Dev\Python Projects\MLOps\phase_1.0\data\raw\ai4i2020.csv')
