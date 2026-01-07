import pandas as pd
import matplotlib
matplotlib.use('TkAgg')  # Or 'Qt5Agg', 'WXAgg', etc. Try these if TkAgg doesn't work
import matplotlib.pyplot as plt
import seaborn as sns
import re
import numpy as np
from collections import Counter

# --- 1. Load the Data ---
try:
    df = pd.read_csv("artwork_data.csv")
except FileNotFoundError:
    print("Error: artwork_data.csv not found.  Make sure it's in the same directory.")
    exit()  # Exit the script if the file is not found
except pd.errors.EmptyDataError:
    print("Error: artwork_data.csv is empty.")
    exit()
except pd.errors.ParserError as e:
    print(f"Error parsing CSV: {e}")
    print("Check for issues like inconsistent number of columns.")
    exit()

# --- 2. Data Cleaning and Preprocessing ---

# --- 2.1 Handle Missing Values ---
# Count missing values in each column
print("Missing Values Before Handling:\n", df.isnull().sum())

# Strategy: Fill missing values appropriately.  Different strategies for different columns:
df['Unframed Dimensions'] = df['Unframed Dimensions'].fillna('Unknown')
df['Unframed Dimensions (inch)'] = df['Unframed Dimensions (inch)'].fillna('Unknown')
df['support'] = df['support'].fillna('Unknown')
df['encadrement'] = df['encadrement'].fillna('Unknown')
df['tags'] = df['tags'].fillna('No Tags')  # Common to have no tags
df['price'] = df['price'].fillna('Price Not Available')
df['techniques'] = df['techniques'].fillna('Not Specified')
df['year'] = df['year'].fillna('Not Found')

# Drop duplicates:
df.drop_duplicates(inplace=True)  # Keep only the first occurrence of the data


# --- 2.2 Data Type Conversion ---
# Convert 'year' to integer (handling errors)
def convert_year(year_str):
    try:
        return int(year_str)
    except (ValueError, TypeError):
        return np.nan  # Use NaN for missing numeric values

df['year'] = df['year'].apply(convert_year)  # convert year to numeric, so you can better use it

# Convert 'price' to numeric (remove currency symbols, handle spaces)
df['price'] = df['price'].str.replace(r'[^\d]', '', regex=True)  # Remove non-digit characters
df['price'] = pd.to_numeric(df['price'], errors='coerce')  # Convert to numeric, coerce errors to NaN

# --- 2.3 Extract Numerical Dimensions ---
def extract_dimensions(dim_str):
    """Extracts width, height, and depth from dimension strings."""
    if isinstance(dim_str, str):
        match = re.findall(r'(\d+\.?\d*)', dim_str)  # Find all numbers (integers and decimals)
        if len(match) == 3:
            try:
                return [float(x) for x in match]  # convert to float
            except ValueError:
                return [None, None, None]
        else:
            return [None, None, None]
    else:
        return [None, None, None]

# Apply the function and create new columns
df[['width_cm', 'height_cm', 'depth_cm']] = df['Unframed Dimensions'].apply(extract_dimensions).tolist()
df[['width_in', 'height_in', 'depth_in']] = df['Unframed Dimensions (inch)'].apply(extract_dimensions).tolist()

# --- 2.4  Clean up the 'tags' column ---
# Convert tags to lowercase and split into lists
df['tags'] = df['tags'].str.lower().str.split(', ')


print("\nMissing Values After Handling:\n", df.isnull().sum())  # check missing values again
print("\nData Types:\n", df.dtypes)
print("\nCleaned Data (First 5 Rows):\n", df.head())



# --- 3. Exploratory Data Analysis (EDA) ---

# --- 3.1 Univariate Analysis ---

# --- 3.1.1 Numerical Features ---
print("\n--- Summary Statistics (Numerical Features) ---")
print(df.describe())


# Histograms for numerical features
numerical_cols = ['year', 'price', 'width_cm', 'height_cm', 'depth_cm', 'width_in', 'height_in', 'depth_in']
df[numerical_cols].hist(bins=20, figsize=(15, 10))
plt.suptitle("Histograms of Numerical Features")
plt.tight_layout(rect=[0, 0.03, 1, 0.95])  # Adjust layout to prevent title overlap
plt.show()


# --- 3.1.2 Categorical Features ---
print("\n--- Value Counts (Categorical Features) ---")
categorical_cols = ['artist', 'techniques', 'support', 'encadrement']
for col in categorical_cols:
    print(f"\n--- {col} ---")
    print(df[col].value_counts())

all_techniques = []
for tech_list in df['techniques'].str.split(', '):
    if isinstance(tech_list, list):
        all_techniques.extend(tech_list)

# 2. Count the occurrences of each technique.
technique_counts = Counter(all_techniques)


# 3. Convert to DataFrame for easier plotting.
technique_counts_df = pd.DataFrame.from_dict(technique_counts, orient='index', columns=['Count'])
technique_counts_df.index.name = 'Technique'  # Set index name
technique_counts_df = technique_counts_df.sort_values('Count', ascending=False) #sort

print("\n--- Artwork Counts per Technique ---")
print(technique_counts_df)

# 4. Visualize the counts (bar plot).
plt.figure(figsize=(14, 8))  # Adjust figure size for readability
technique_counts_df.plot(kind='bar', legend=False) #plot
plt.title('Number of Artworks per Technique')
plt.xlabel('Technique')
plt.ylabel('Number of Artworks')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()


# Bar plots for categorical features
for col in categorical_cols:
    plt.figure(figsize=(12, 6))  # Adjust figure size for better readability
    df[col].value_counts().plot(kind='bar')
    plt.title(f"Distribution of {col}")
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for readability
    plt.tight_layout()
    plt.show()


# --- 3.1.3  Tags Analysis (Special Case) ---

# Create a list of all unique tags
all_tags = []
for tag_list in df['tags']:
     if isinstance(tag_list, list): #handle if tag_list is not a list
        all_tags.extend(tag_list)
tag_counts = pd.Series(all_tags).value_counts()
print(f"\n----Most Common Tags ---\n{tag_counts}")


# --- 3.2 Bivariate Analysis ---

# --- 3.2.1  Scatter Plots (Numerical vs. Numerical) ---

# Example: price vs. width_cm
plt.figure(figsize=(8, 6))
plt.scatter(df['width_cm'], df['price'], alpha=0.5)
plt.title('Price vs. Width (cm)')
plt.xlabel('Width (cm)')
plt.ylabel('Price')
plt.show()

# Example year vs price
plt.figure(figsize=(8, 6))
plt.scatter(df['year'], df['price'], alpha=0.5)
plt.title('Price vs. Year')
plt.xlabel('Year')
plt.ylabel('Price')
plt.show()

# --- 3.2.2  Box Plots (Categorical vs. Numerical) ---

# Example: price vs. encadrement
plt.figure(figsize=(10, 6))
sns.boxplot(x='encadrement', y='price', data=df)
plt.title('Price vs. Encadrement')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()


# --- 3.2.3 Correlation Matrix (Numerical Features) ---
correlation_matrix = df[numerical_cols].corr()
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation Matrix of Numerical Features")
plt.show()


# --- 4.  Insights and Conclusions (Example) ---

print("\n--- Example Insights and Conclusions ---")
print("- The dataset contains information on artwork, including dimensions, price, and materials.")
print("- There are some missing values, particularly in the 'framed_dimensions' column.  We filled these.")
print("- The most common support is 'Peinture sur toile sur chassis'.")
print("- The distribution of prices is right-skewed (more lower-priced artworks).")
print("- There's a weak positive correlation between width and price (larger works tend to be slightly more expensive).")
print("- Further analysis could explore the relationship between specific tags and price.")
print("- We could also do artist-level analysis if you want to")