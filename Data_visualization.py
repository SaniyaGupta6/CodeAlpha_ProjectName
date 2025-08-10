import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

DATA_PATH = r"D:\codeaplha1\books_dataset.csv"

try:
    df = pd.read_csv(DATA_PATH)
    print("Data loaded successfully!")
    print("Available columns:", df.columns.tolist())
except FileNotFoundError:
    print("File not found. Please check the path and try again.")
    raise

df_renamed = df.rename(columns={'Title': 'T', 'Price': 'P', 'Availability': 'A'})

def to_float_price(s):
    if pd.isna(s):
        return None
    s = str(s).strip()
    s = (s.replace('Rs.', '').replace('Rs ', '').replace('Rs', '')
             .replace(',', '').strip())
    try:
        return float(s)
    except ValueError:
        return None

df_renamed['P'] = df_renamed['P'].apply(to_float_price)
df_renamed = df_renamed.dropna(subset=['P'])

sns.set(style="whitegrid")

def plot_bar():
    plt.figure(figsize=(10,6))
    sns.barplot(x='T', y='P', data=df_renamed)
    plt.title('Bar Plot: Price by Title')
    plt.xlabel('Title (T)')
    plt.ylabel('Price (P)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def plot_line():
    plt.figure(figsize=(10,6))
    plt.plot(df_renamed.index, df_renamed['P'], marker='o')
    plt.title('Line Plot: Price over Index')
    plt.xlabel('Index')
    plt.ylabel('Price (P)')
    plt.tight_layout()
    plt.show()

def plot_hist():
    plt.figure(figsize=(8,5))
    sns.histplot(df_renamed['P'], bins=20, kde=True)
    plt.title('Histogram of Price (P)')
    plt.xlabel('Price (P)')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.show()

def plot_scatter():
    avail_unique = df_renamed['A'].unique()
    mapping = {val: i for i, val in enumerate(avail_unique)}
    df_scatter = df_renamed.copy()
    df_scatter['A_num'] = df_scatter['A'].map(mapping)

    plt.figure(figsize=(8,6))
    sns.scatterplot(x='T', y='P', hue='A', data=df_scatter, palette='viridis')
    plt.title('Scatter: Price (P) vs Title (T) colored by Availability (A)')
    plt.xlabel('Title (T)')
    plt.ylabel('Price (P)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

plot_bar()
plot_line()
plot_hist()
plot_scatter()

print("Plots generated. If you need adjustments (e.g., a real time column or different mappings), tell me.")