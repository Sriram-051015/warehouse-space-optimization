import pandas as pd
import os

priority_file = "data/processed/warehouse_priority.csv"
location_file = "data/processed/warehouse_locations.csv"

output_file = "data/processed/final_warehouse_analytics.csv"

print("\n===== CREATING FINAL ANALYTICS DATASET =====")

# ============================================================
# STEP 1: LOAD DATA
# ============================================================

priority = pd.read_csv(
    priority_file
)

locations = pd.read_csv(
    location_file
)

print("Priority records:", len(priority))
print("Location records:", len(locations))

# ============================================================
# STEP 2: MERGE DATASETS
# ============================================================

data = pd.merge(
    priority,
    locations[
        [
            "SKU",
            "main_storage_location",
            "location_pick_count"
        ]
    ],
    on="SKU",
    how="left"
)

# ============================================================
# STEP 3: CREATE RECOMMENDED ZONE
# ============================================================

def recommend_zone(priority):

    if priority == "High Priority":
        return "ZONE_A"

    elif priority == "Medium Priority":
        return "ZONE_B"

    else:
        return "ZONE_C"


data["recommended_zone"] = data[
    "storage_priority"
].apply(recommend_zone)

# ============================================================
# STEP 4: SPACE SHARE
# ============================================================

total_volume = data[
    "product_volume"
].sum()

data["space_percentage"] = (
    data["product_volume"]
    / total_volume
    * 100
)

# ============================================================
# STEP 5: RELOCATION RECOMMENDATION
# ============================================================

data["relocation_recommended"] = (
    data["storage_priority"] != "Low Priority"
)

# ============================================================
# STEP 6: SELECT FINAL COLUMNS
# ============================================================

final_data = data[
    [
        "SKU",
        "HGT1",
        "WID1",
        "DPTH1",
        "product_volume",
        "pick_count",
        "total_quantity_picked",
        "movement_frequency",
        "movement_category",
        "cluster",
        "storage_priority_score",
        "storage_priority",
        "main_storage_location",
        "location_pick_count",
        "recommended_zone",
        "relocation_recommended",
        "space_percentage"
    ]
].copy()

# ============================================================
# STEP 7: SAVE DATASET
# ============================================================

os.makedirs(
    "data/processed",
    exist_ok=True
)

final_data.to_csv(
    output_file,
    index=False
)

# ============================================================
# STEP 8: DISPLAY SUMMARY
# ============================================================

print("\n===== FINAL DATASET =====")

print("Rows:", len(final_data))
print("Columns:", len(final_data.columns))

print("\n===== COLUMNS =====")

print(
    final_data.columns.tolist()
)

print("\n===== MISSING VALUES =====")

print(
    final_data.isnull().sum()
)

print("\n===== FIRST 10 ROWS =====")

print(
    final_data.head(10)
)

print("\n===== OUTPUT SAVED =====")

print(output_file)

print("\n===== FINAL DATASET CREATION COMPLETE =====")