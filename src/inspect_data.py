import pandas as pd

# ============================================================
# PICKS DATASET INSPECTION
# ============================================================

pick_file = "data/raw/picks/picks.csv"

print("\n===== READING PICKS DATASET =====")

# Skip the second header/description row.
# Inspect only the first 100,000 real records for now.
picks = pd.read_csv(
    pick_file,
    skiprows=[1],
    nrows=100000,
    on_bad_lines="skip"
)

# ============================================================
# BASIC INFORMATION
# ============================================================

print("\n===== PICKS DATASET =====")
print("Rows inspected:", picks.shape[0])
print("Columns:", picks.shape[1])

# ============================================================
# COLUMN NAMES
# ============================================================

print("\n===== COLUMN NAMES =====")
print(picks.columns.tolist())

# ============================================================
# FIRST 5 ROWS
# ============================================================

print("\n===== FIRST 5 ROWS =====")
print(picks.head())

# ============================================================
# DATA TYPES
# ============================================================

print("\n===== DATA TYPES =====")
print(picks.dtypes)

# ============================================================
# MISSING VALUES
# ============================================================

print("\n===== MISSING VALUES =====")
print(picks.isnull().sum())

# ============================================================
# UNIQUE VALUES
# ============================================================

print("\n===== UNIQUE VALUES =====")

for column in picks.columns:
    print(
        column,
        "->",
        picks[column].nunique()
    )

print("\n===== INSPECTION COMPLETE =====")