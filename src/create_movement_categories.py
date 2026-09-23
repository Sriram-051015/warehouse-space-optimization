import pandas as pd

# ============================================================
# FILE PATHS
# ============================================================

input_file = "data/processed/warehouse_optimization_data.csv"
output_file = "data/processed/warehouse_optimization_data.csv"

print("\n===== CREATING MOVEMENT CATEGORIES =====")

# ============================================================
# STEP 1: READ DATA
# ============================================================

data = pd.read_csv(input_file)

print("Rows:", len(data))

# ============================================================
# STEP 2: CALCULATE MOVEMENT PERCENTILES
# ============================================================

low_threshold = data["movement_frequency"].quantile(0.33)
high_threshold = data["movement_frequency"].quantile(0.66)

print("\n===== MOVEMENT THRESHOLDS =====")
print("Low threshold:", low_threshold)
print("High threshold:", high_threshold)

# ============================================================
# STEP 3: CREATE MOVEMENT CATEGORY
# ============================================================

def classify_movement(value):

    if value <= low_threshold:
        return "Low Movement"

    elif value <= high_threshold:
        return "Medium Movement"

    else:
        return "High Movement"


data["movement_category"] = data[
    "movement_frequency"
].apply(classify_movement)

# ============================================================
# STEP 4: CHECK CATEGORY COUNTS
# ============================================================

print("\n===== MOVEMENT CATEGORY COUNTS =====")

print(
    data["movement_category"].value_counts()
)

# ============================================================
# STEP 5: SAVE UPDATED DATASET
# ============================================================

data.to_csv(
    output_file,
    index=False
)

print("\n===== DATASET UPDATED =====")
print(output_file)

print("\n===== PROCESS COMPLETE =====")