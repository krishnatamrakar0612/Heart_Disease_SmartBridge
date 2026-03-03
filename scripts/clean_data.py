import pandas as pd
from pathlib import Path

BASE_DIR   = Path(__file__).resolve().parent.parent
INPUT_FILE  = BASE_DIR / "data" / "Heart_disease_raw.csv"
OUTPUT_FILE = BASE_DIR / "data" / "Heart_disease_cleaned.csv"

def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        print(f"Data loaded successfully. Shape: {df.shape}")
        return df
    except Exception as e:
        print("Error loading file:", e)
        return None

def standardize_column_names(df):
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )
    print("Column names standardized:", list(df.columns))
    return df

def remove_duplicates(df):
    initial_count = df.shape[0]
    df = df.drop_duplicates()
    removed = initial_count - df.shape[0]
    print(f"Removed {removed} duplicate rows. Remaining: {df.shape[0]}")
    return df

def handle_missing_values(df):
    missing_before = df.isnull().sum().sum()

    num_cols = df.select_dtypes(include=["int64", "float64"]).columns
    for col in num_cols:
        df[col] = df[col].fillna(df[col].median())

    cat_cols = df.select_dtypes(include=["object"]).columns
    for col in cat_cols:
        df[col] = df[col].fillna(df[col].mode()[0])

    missing_after = df.isnull().sum().sum()
    print(f"Missing values handled. Before: {missing_before} -> After: {missing_after}")
    return df

def handle_bmi_outliers(df):
    if "bmi" not in df.columns:
        return df

    q1  = df["bmi"].quantile(0.25)
    q3  = df["bmi"].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    outliers = df[(df["bmi"] < lower) | (df["bmi"] > upper)].shape[0]
    df["bmi"] = df["bmi"].clip(lower=lower, upper=upper)

    print(f"BMI outliers clipped. {outliers} values adjusted. Range: [{lower:.2f}, {upper:.2f}]")
    return df

def simplify_diabetic(df):
    if "diabetic" not in df.columns:
        return df

    before = df["diabetic"].value_counts().to_dict()

    df["diabetic"] = df["diabetic"].replace({
        "Yes (during pregnancy)": "Yes",
        "No, borderline diabetes": "No"
    })

    after = df["diabetic"].value_counts().to_dict()
    print("Diabetic column simplified.")
    print(f"   Before: {before}")
    print(f"   After : {after}")
    return df

def fix_data_types(df):
    if "heartdisease" in df.columns:
        df["heartdisease"] = df["heartdisease"].astype(str).str.strip()

    if "agecategory" in df.columns:
        df["agecategory"] = df["agecategory"].astype(str).str.strip()

    for col in ["bmi", "physicalhealth", "mentalhealth", "sleeptime"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    print("Data types fixed.")
    return df

def encode_categorical(df):
    binary_cols = [
        "smoking", "alcoholdrinking", "stroke", "diffwalking",
        "physicalactivity", "asthma", "kidneydisease", "skincancer"
    ]
    for col in binary_cols:
        if col in df.columns:
            df[col] = df[col].map({"Yes": 1, "No": 0}).fillna(df[col])

    if "sex" in df.columns:
        df["sex"] = df["sex"].map({"Male": 1, "Female": 0}).fillna(df["sex"])

    print("Categorical encoding applied.")
    print("   Encoded columns:", binary_cols + ["sex"])
    return df

def print_summary(df):
    print("\nFinal Dataset Summary")
    print(f"   Shape        : {df.shape}")
    print(f"   Nulls        : {df.isnull().sum().sum()}")
    print(f"   Duplicates   : {df.duplicated().sum()}")
    print(f"\n   Column dtypes:\n{df.dtypes}")
    print(f"\n   HeartDisease : {df['heartdisease'].value_counts().to_dict()}")
    print(f"   Sex          : {df['sex'].value_counts().to_dict()}")
    print(f"   Diabetic     : {df['diabetic'].value_counts().to_dict()}")
    print(f"   BMI range    : {df['bmi'].min():.2f} - {df['bmi'].max():.2f}")

def main():
    print("=" * 50)
    print("Heart Disease Data Cleaning Pipeline")
    print("=" * 50)

    df = load_data(INPUT_FILE)

    if df is not None:
        df = standardize_column_names(df)
        df = remove_duplicates(df)
        df = handle_missing_values(df)
        df = handle_bmi_outliers(df)
        df = simplify_diabetic(df)
        df = fix_data_types(df)
        df = encode_categorical(df)

        print_summary(df)

        df.to_csv(OUTPUT_FILE, index=False)
        print(f"\nCleaned data saved to: {OUTPUT_FILE}")

    print("=" * 50)


if __name__ == "__main__":
    main()