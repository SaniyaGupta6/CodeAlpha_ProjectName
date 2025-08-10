import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
path = input("Enter the path to your CSV data file (e.g., 'your_data.csv'): ").strip()
df = pd.read_csv(path)

print("Data loaded successfully!")
print("Available columns:", df.columns.tolist())

def choose_column(prompt, valid_columns, allow_empty=False):
    while True:
        val = input(prompt).strip()
        if allow_empty and val == "":
            return None
        # If user enters a number, map to position
        if val.isdigit():
            idx = int(val) - 1
            if 0 <= idx < len(valid_columns):
                return valid_columns[idx]
            else:
                print("Index out of range. Try again.")
                continue
        # Otherwise, treat as column name
        if val in valid_columns:
            return val
        else:
            print("Column not found. Available columns:", valid_columns)

cols = df.columns.tolist()

# 1) categorical column for bar plot
cat_col = choose_column("Enter the categorical column for bar plot (or leave blank to skip): ", cols, allow_empty=True)
# 2) numeric column for bar plot
num_col = choose_column("Enter the numeric column for bar plot: ", cols)
# 3) time-related column for line plot (optional)
time_col = choose_column("Enter the time-related column for line plot (or leave blank to skip): ", cols, allow_empty=True)
line_y_col = None
if time_col:
    line_y_col = choose_column("Enter the measurement column for line plot: ", cols)

# 4) numeric column for histogram
hist_col = choose_column("Enter the numeric column for histogram: ", cols)

# 5) first feature for scatter plot
scatter_x = choose_column("Enter the first feature for scatter plot: ", cols)
# 6) second feature for scatter plot
scatter_y = choose_column("Enter the second feature for scatter plot: ", cols)

# Safety: build plots only with valid combos
def safe_barplot(cat_col, val_col):
    if cat_col is None or val_col is None:
        print("Bar plot skipped due to missing columns.")
        return
    if cat_col not in df.columns or val_col not in df.columns:
        print("Bar plot skipped due to invalid columns.")
        return
    plt.figure(figsize=(6,4))
    sns.barplot(x=cat_col, y=val_col, data=df)
    plt.title(f"Bar plot: {val_col} by {cat_col}")
    plt.tight_layout()
    plt.show()

def safe_hist(col):
    if col is None or col not in df.columns:
        print("Histogram skipped due to invalid column.")
        return
    plt.figure(figsize=(6,4))
    sns.histplot(df[col], kde=True)
    plt.title(f"Histogram of {col}")
    plt.tight_layout()
    plt.show()

def safe_scatter(xcol, ycol):
    if xcol is None or ycol is None:
        print("Scatter plot skipped due to missing columns.")
        return
    if xcol not in df.columns or ycol not in df.columns:
        print("Scatter plot skipped due to invalid columns.")
        return
    plt.figure(figsize=(6,4))
    sns.scatterplot(x=xcol, y=ycol, data=df)
    plt.title(f"Scatter: {xcol} vs {ycol}")
    plt.tight_layout()
    plt.show()

def safe_line(xcol, ycol):
    if xcol is None or ycol is None:
        print("Line plot skipped due to missing columns.")
        return
    if xcol not in df.columns or ycol not in df.columns:
        print("Line plot skipped due to invalid columns.")
        return
    plt.figure(figsize=(6,4))
    sns.lineplot(x=xcol, y=ycol, data=df)
    plt.title(f"Line plot: {ycol} over {xcol}")
    plt.tight_layout()
    plt.show()

# Generate plots
safe_barplot(cat_col, num_col)
safe_line(time_col, line_y_col)
safe_hist(hist_col)
safe_scatter(scatter_x, scatter_y)

print("Plotting complete.")