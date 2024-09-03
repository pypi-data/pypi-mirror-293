# pandasProfilingManual.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# General Statistics
def general_statistics(df):
    print("General Statistics:")
    print(f"Number of variables: {df.shape[1]}")
    print(f"Number of observations: {df.shape[0]}")
    print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    missing_values_summary(df)
    print()

def missing_values_summary(df):
    missing_values = df.isnull().sum()
    missing_percent = (missing_values / len(df)) * 100
    print("Missing Values Summary:")
    print(pd.DataFrame({
        'Missing Values': missing_values,
        'Percentage': missing_percent
    }).sort_values(by='Missing Values', ascending=False))
    print()

# Per Variable Analysis
def per_variable_analysis(df):
    print("Per Variable Analysis:")
    for column in df.columns:
        print(f"\nColumn: {column}")
        print(f"Type: {df[column].dtype}")
        if pd.api.types.is_numeric_dtype(df[column]):
            print(df[column].describe())
            distribution_plot(df[column])
        elif pd.api.types.is_categorical_dtype(df[column]) or df[column].dtype == object:
            print(df[column].value_counts())
            bar_plot(df[column])
        elif pd.api.types.is_bool_dtype(df[column]):
            print(df[column].value_counts())
            bar_plot(df[column])
        print(f"Missing Values: {df[column].isnull().sum()} ({df[column].isnull().mean() * 100:.2f}%)")
        print(f"Unique Values: {df[column].nunique()}")
    print()

def distribution_plot(column):
    plt.figure(figsize=(10, 6))
    sns.histplot(column.dropna(), kde=True)
    plt.title(f'Distribution of {column.name}')
    plt.show()

def bar_plot(column):
    plt.figure(figsize=(10, 6))
    sns.countplot(y=column)
    plt.title(f'Bar Plot of {column.name}')
    plt.show()

# Correlation Analysis
def correlation_analysis(df):
    print("Correlation Analysis:")
    numeric_df = df.select_dtypes(include=[np.number])  # Filter numeric columns only
    correlation_matrix = numeric_df.corr(method='pearson')
    print(correlation_matrix)
    correlation_heatmap(correlation_matrix)

def correlation_heatmap(corr_matrix):
    plt.figure(figsize=(12, 8))
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm')
    plt.title('Correlation Heatmap')
    plt.show()

# Warnings and Alerts
def warnings_and_alerts(df):
    print("Warnings and Alerts:")
    for column in df.columns:
        if pd.api.types.is_categorical_dtype(df[column]) or df[column].dtype == object:
            if df[column].nunique() > 50:
                print(f"High Cardinality Warning: {column} has {df[column].nunique()} unique values.")
        if df[column].isnull().mean() > 0.5:
            print(f"High Missing Values Warning: {column} has {df[column].isnull().mean() * 100:.2f}% missing values.")
        if df[column].nunique() == 1:
            print(f"Constant Column Warning: {column} has a single unique value.")
    duplicate_rows = df[df.duplicated()]
    if not duplicate_rows.empty:
        print(f"Duplicate Rows Warning: Found {duplicate_rows.shape[0]} duplicate rows.")
    print()

# Outlier Detection
def outlier_detection(df):
    print("Outlier Detection:")
    for column in df.select_dtypes(include=[np.number]).columns:
        q1 = df[column].quantile(0.25)
        q3 = df[column].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
        if not outliers.empty:
            print(f"Outliers detected in {column}:")
            print(outliers)
    print()

def data_types_memory_usage(df):
    print("Data Types and Memory Usage:")
    dtypes = df.dtypes
    mem_usage = df.memory_usage(deep=True) / 1024**2  # Convert to MB
    data_types_mem_usage = pd.DataFrame({
        'Data Type': dtypes,
        'Memory Usage (MB)': mem_usage
    })
    print(data_types_mem_usage)
    print()

def top_value_summary(df):
    print("Top Values in Categorical Columns:")
    for column in df.select_dtypes(include=['object', 'category']):
        print(f"\nColumn: {column}")
        print(df[column].value_counts().head(10))
    print()

def date_time_analysis(df):
    print("Date-Time Analysis:")
    date_columns = df.select_dtypes(include=['datetime64']).columns
    for column in date_columns:
        print(f"\nColumn: {column}")
        print(df[column].describe())
        print(f"Range: {df[column].min()} to {df[column].max()}")
    print()

def custom_aggregations(df):
    print("Custom Aggregations:")
    numeric_df = df.select_dtypes(include=[np.number])
    for column in numeric_df.columns:
        median = numeric_df[column].median()
        variance = numeric_df[column].var()
        print(f"{column} - Median: {median}, Variance: {variance}")
    print()


def class_imbalance(df, target_column):
    if target_column in df.columns:
        print("Class Imbalance:")
        print(df[target_column].value_counts(normalize=True))
        print()

def group_statistics(df, group_column):
    if group_column in df.columns:
        print(f"Group Statistics by {group_column}:")
        grouped_df = df.groupby(group_column).describe()
        print(grouped_df)
        print()

def save_plot(plot_func, filename):
    plot_func()
    plt.savefig(filename)
    plt.close()


def distribution_plot(column):
    plt.figure(figsize=(10, 6))
    sns.histplot(column.dropna(), kde=True)
    plt.title(f'Distribution of {column.name}')
    save_plot(plt.gcf, f'{column.name}_distribution_plot.png')


def bar_plot(column):
    plt.figure(figsize=(10, 6))
    sns.countplot(y=column)
    plt.title(f'Bar Plot of {column.name}')
    save_plot(plt.gcf, f'{column.name}_bar_plot.png')

def skewness_and_kurtosis(df):
    print("Skewness and Kurtosis:")
    for column in df.select_dtypes(include=[np.number]).columns:
        skewness = df[column].skew()
        kurtosis = df[column].kurt()
        print(f"{column} - Skewness: {skewness:.2f}, Kurtosis: {kurtosis:.2f}")
    print()

def detailed_categorical_summary(df):
    print("Detailed Categorical Summary:")
    for column in df.select_dtypes(include=['object', 'category']):
        print(f"\nColumn: {column}")
        value_counts = df[column].value_counts()
        proportions = df[column].value_counts(normalize=True)
        print(pd.DataFrame({'Count': value_counts, 'Proportion': proportions}))
    print()


def temporal_analysis(df):
    print("Temporal Analysis:")
    date_columns = df.select_dtypes(include=['datetime64']).columns
    for column in date_columns:
        df[column].dt.month.value_counts().sort_index().plot(kind='bar', title=f'{column} - Monthly Distribution')
        plt.show()
        df[column].dt.dayofweek.value_counts().sort_index().plot(kind='bar', title=f'{column} - Weekly Distribution')
        plt.show()
    print()


def data_sampling(df, sample_size=100):
    print("Data Sampling:")
    print(df.sample(n=sample_size))
    print()


def data_validation(df):
    print("Data Validation:")
    for column in df.columns:
        if df[column].dtype == 'object':
            invalid_entries = df[column].apply(lambda x: isinstance(x, str) and not x.strip()).sum()
            if invalid_entries > 0:
                print(f"Column {column} has {invalid_entries} invalid string entries.")
    print()


def imputation_suggestions(df):
    print("Imputation Suggestions:")
    missing_data = df.isnull().sum()
    for column in df.columns:
        if missing_data[column] > 0:
            if pd.api.types.is_numeric_dtype(df[column]):
                print(f"Column {column} - Consider imputation with mean or median.")
            elif pd.api.types.is_categorical_dtype(df[column]) or df[column].dtype == object:
                print(f"Column {column} - Consider imputation with the most frequent value or create a 'missing' category.")
    print()




def profile_report(df, target_column=None, group_column=None):
    general_statistics(df)
    per_variable_analysis(df)
    correlation_analysis(df)
    warnings_and_alerts(df)
    outlier_detection(df)
    data_types_memory_usage(df)
    top_value_summary(df)
    date_time_analysis(df)
    custom_aggregations(df)
    temporal_analysis(df)
    detailed_categorical_summary(df)
    data_sampling(df, sample_size=100)
    data_validation(df)
    imputation_suggestions(df)
    skewness_and_kurtosis(df)
    if target_column:
        class_imbalance(df, target_column)
    if group_column:
        group_statistics(df, group_column)
