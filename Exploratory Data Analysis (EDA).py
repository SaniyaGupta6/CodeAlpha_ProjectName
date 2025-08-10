import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Optional: for a quick, interactive profiling report
try:
    from pandas_profiling import ProfileReport
    HAS_PROFILING = True
except Exception:
    HAS_PROFILING = False

# 1) CONFIG: dataset path and analysis toggles
DATA_PATH = r"data/your_dataset.csv"  # <- update this to your CSV path
OUTPUT_DIR = "eda_reports"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Toggles
GENERATE_PROFILE = True  # if pandas_profiling is available, generate a report
SHOW_PLOTS = True        # set to False if running headless
SAVE_PLOTS = True        # save plots to OUTPUT_DIR
PLOT_FORMAT = "png"      # e.g., 'png', 'pdf', etc.

# 2) LOAD DATA
try:
    df = pd.read_csv(DATA_PATH)
    print("Data loaded successfully.")
except FileNotFoundError:
    print(f"File not found: {DATA_PATH}")
    sys.exit(1)
except pd.errors.ParserError as e:
    print(f"CSV parsing error: {e}")
    sys.exit(1)

print("Columns:", list(df.columns))
print("\nData info:")
print(df.info())
print("\nFirst few rows:")
print(df.head())

# 3) CLEANING & TYPING (adjust to your dataset)
# a) Detect basic types
dtypes = df.dtypes
print("\nDtypes:")
print(dtypes)

# b) Handle missing values summary
missing = df.isnull().mean().sort_values(ascending=False)
print("\nMissing value proportions (per column):")
print(missing)

# c) Convert potential numeric columns that are typed as object
# Example: if a column looks numeric but is object due to commas/crefix
def try_cast_numeric(col: pd.Series):
    s = col.astype(str).str.strip()
    s = s.str.replace(r"[,$€¥₹Rs]", "", regex=True)
    s = s.str.replace(",", "", regex=False)
    return pd.to_numeric(s, errors="coerce")

for col in df.columns:
    # heuristic: if object type and a large portion can be numeric
    if df[col].dtype == "object":
        numeric_like = pd.to_numeric(df[col].str.replace(",", "", regex=False).str.replace(r"[^\d\.\-]", "", regex=True), errors="coerce")
        if numeric_like.notnull().mean() > 0.5:
            df[col] = numeric_like
            print(f"Converted column '{col}' to numeric.")
        else:
            # keep as is
            pass

# d) Example: parse date/time columns if any (best effort)
for col in df.columns:
    if "date" in col.lower() or "time" in col.lower():
        try:
            df[col] = pd.to_datetime(df[col], errors="coerce")
            print(f"Converted column '{col}' to datetime.")
        except Exception:
            pass

# e) Create a clean copy for analysis
df_clean = df.copy()

# f) Optional: drop or fill missing values (customize as needed)
# Simple approach: fill numeric columns with median, categorical with mode
for col in df_clean.columns:
    if pd.api.types.is_numeric_dtype(df_clean[col]):
        df_clean[col] = df_clean[col].fillna(df_clean[col].median())
    else:
        df_clean[col] = df_clean[col].fillna(df_clean[col].mode().iloc[0])

# 4) DESCRIPTIVE STATISTICS
print("\nDescriptive statistics (numeric columns):")
print(df_clean.describe(include=[np.number]).transpose())

print("\nDescriptive statistics (all columns):")
print(df_clean.describe(include="all").transpose())

# Optional: correlation matrix for numeric features
numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
if len(numeric_cols) >= 2:
    corr = df_clean[numeric_cols].corr()
    print("\nCorrelation matrix:")
    print(corr)

# 5) UNIVARIATE VISUALIZATIONS
sns.set(style="whitegrid", context="notebook")

plot_paths = []

def save_or_show(plot_func, fname):
    plt.figure(figsize=(8, 5))
    plot_func()
    if SAVE_PLOTS:
        path = os.path.join(OUTPUT_DIR, fname)
        plt.savefig(path, format=PLOT_FORMAT, bbox_inches="tight")
        plot_paths.append(path)
        print(f"Saved plot: {path}")
    if SHOW_PLOTS:
        plt.show()
    plt.close()

# Example plots (adapt to your columns)
# 5a) Univariate distribution for numeric columns
def plot_numeric_distributions():
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
    n = len(numeric_cols)
    plt.figure(figsize=(6 * max(1, n), 4))
    for i, col in enumerate(numeric_cols):
        plt.subplot(1, n, i + 1)
        sns.histplot(df_clean[col], kde=True, bins=20)
        plt.title(col)
    plt.tight_layout()

# 5b) Categorical value counts
def plot_categorical_counts():
    cat_cols = df_clean.select_dtypes(include=['object', 'bool']).columns
    if len(cat_cols) == 0:
        return
    plt.figure(figsize=(6 * len(cat_cols), 4))
    for i, col in enumerate(cat_cols):
        plt.subplot(1, len(cat_cols), i + 1)
        sns.countplot(y=df_clean[col], order=df_clean[col].value_counts().index)
        plt.title(col)
    plt.tight_layout()

# 5c) Pairwise relationships (limited to top 5 numeric vars to keep it light)
def plot_pairwise():
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
    top5 = numeric_cols[:5]
    if len(top5) < 2:
        return
    sns.pairplot(df_clean[top5])

# Run univariate visualizations
save_or_show(plot_numeric_distributions, "univariate_numeric_distributions.png")
save_or_show(plot_categorical_counts, "categorical_counts.png")
# Optional
# save_or_show(plot_pairwise, "pairwise_relationships.png")

# 6) BIVARIATE VISUALIZATIONS (correlation, plots by groups)
def plot_bar_by_group(x_col, y_col, data=None):
    data = data or df_clean
    plt.figure(figsize=(10, 6))
    sns.barplot(x=x_col, y=y_col, data=data)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

def plot_box_by_group(x_col, y_col, data=None):
    data = data or df_clean
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=x_col, y=y_col, data=data)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

# Example: numeric vs categorical
def plot_numeric_vs_categorical():
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
    cat_cols = df_clean.select_dtypes(include=['object']).columns
    if len(numeric_cols) > 0 and len(cat_cols) > 0:
        for c in cat_cols:
            plt.figure(figsize=(8, 6))
            sns.boxplot(x=c, y=numeric_cols[0], data=df_clean)
            plt.title(f"{numeric_cols[0]} by {c}")
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            if SAVE_PLOTS:
                path = os.path.join(OUTPUT_DIR, f"{numeric_cols[0]}_by_{c}.png")
                plt.savefig(path, bbox_inches="tight")
                print(f"Saved plot: {path}")
            if SHOW_PLOTS:
                plt.show()
            plt.close()

# 7) Quick profiling report (optional)
if GENERATE_PROFILE and HAS_PROFILING:
    profile = ProfileReport(df, title="EDA Profiling Report", explorative=True)
    profile.to_file(os.path.join(OUTPUT_DIR, "profile_report.html"))

# 8) Execute a basic suite of plots
plot_bar_by_group("T" if "T" in df_clean.columns else df_clean.columns[0], 
                  "P" if "P" in df_clean.columns else df_clean.columns[1],
                  data=df_clean)
plot_box_by_group("T" if "T" in df_clean.columns else df_clean.columns[0], 
                  "P" if "P" in df_clean.columns else df_clean.columns[1],
                  data=df_clean)

# 9) Summary
print("\nEDA complete. Output files (plots, if saved) are in:", OUTPUT_DIR)
