import pandas as pd
import numpy as np


# ===============================
# CONFIGURATION
# ===============================

INPUT_FILE = "../data/Heart_disease_raw.csv"     # Raw dataset file
OUTPUT_FILE = "../data/Heart_disease_cleaned.csv"  # Cleaned dataset file


# ===============================
# LOAD DATA
# ===============================

def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        print("✅ Data loaded successfully.")
        return df
    except Exception as e:
        print("❌ Error loading file:", e)
        return None


# ===============================
# STANDARDIZE COLUMN NAMES
# ===============================

def standardize_column_names(df):
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )
    print("✅ Column names standardized.")
    return df


# ===============================
# REMOVE DUPLICATES
# ===============================

def remove_duplicates(df):
    initial_count = df.shape[0]
    df = df.drop_duplicates()
    final_count = df.shape[0]
    print(f"✅ Removed {initial_count - final_count} duplicate rows.")
    return df


# ===============================
# HANDLE MISSING VALUES
# ===============================

def handle_missing_values(df):

    # Numerical columns → Fill with median
    num_cols = df.select_dtypes(include=['int64', 'float64']).columns
    for col in num_cols:
        df[col].fillna(df[col].median(), inplace=True)

    # Categorical columns → Fill with mode
    cat_cols = df.select_dtypes(include=['object']).columns
    for col in cat_cols:
        df[col].fillna(df[col].mode()[0], inplace=True)

    print("✅ Missing values handled.")
    return df


# ===============================
# FIX DATA TYPES
# ===============================

def fix_data_types(df):

    # Convert common columns if they exist
    if 'age' in df.columns:
        df['age'] = df['age'].astype(int)

    if 'sex' in df.columns:
        df['sex'] = df['sex'].astype(str)

    if 'target' in df.columns:
        df['target'] = df['target'].astype(int)

    print("✅ Data types standardized.")
    return df


# ===============================
# ENCODE CATEGORICAL VARIABLES
# ===============================

def encode_categorical(df):

    # Example mappings (modify based on dataset)
    if 'sex' in df.columns:
        df['sex'] = df['sex'].map({'Male': 1, 'Female': 0}).fillna(df['sex'])

    if 'smoking' in df.columns:
        df['smoking'] = df['smoking'].map({'Yes': 1, 'No': 0}).fillna(df['smoking'])

    print("✅ Categorical encoding applied (if applicable).")
    return df


# ===============================
# MAIN CLEANING PIPELINE
# ===============================

def main():
    df = load_data(INPUT_FILE)

    if df is not None:
        df = standardize_column_names(df)
        df = remove_duplicates(df)
        df = handle_missing_values(df)
        df = fix_data_types(df)
        df = encode_categorical(df)

        df.to_csv(OUTPUT_FILE, index=False)
        print(f"🎉 Cleaned data saved as '{OUTPUT_FILE}'")
        print("Final Dataset Shape:", df.shape)


if __name__ == "__main__":
    main()