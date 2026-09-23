import pandas as pd

# ============================================================
# FILE PATHS
# ============================================================

priority_file = "data/processed/warehouse_priority.csv"
location_file = "data/processed/warehouse_locations.csv"

output_file = "results/warehouse_placement_recommendations.csv"

print("\n===== GENERATING PLACEMENT RECOMMENDATIONS =====")

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
# STEP 2: MERGE PRIORITY WITH CURRENT LOCATION
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
# STEP 3: ASSIGN RECOMMENDED STORAGE ZONE
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
# STEP 4: DETERMINE RELOCATION REQUIREMENT
# ============================================================

# The current location is retained as the reference.
# We mark the product for relocation when it has a
# valid current location and its priority requires
# a different access zone.

data["relocation_recommended"] = (
    data["storage_priority"] != "Low Priority"
)

# ============================================================
# STEP 5: CREATE RECOMMENDATION REASON
# ============================================================

def create_reason(row):

    if row["storage_priority"] == "High Priority":
        return (
            "High movement/space priority; "
            "place in an easily accessible zone."
        )

    elif row["storage_priority"] == "Medium Priority":
        return (
            "Moderate movement/space priority; "
            "place in a standard access zone."
        )

    else:
        return (
            "Lower movement priority; "
            "can use lower-access storage."
        )


data["recommendation_reason"] = data.apply(
    create_reason,
    axis=1
)

# ============================================================
# STEP 6: SELECT FINAL COLUMNS
# ============================================================

recommendations = data[
    [
        "SKU",
        "HGT1",
        "WID1",
        "DPTH1",
        "product_volume",
        "movement_frequency",
        "movement_category",
        "storage_priority_score",
        "storage_priority",
        "main_storage_location",
        "location_pick_count",
        "recommended_zone",
        "relocation_recommended",
        "recommendation_reason"
    ]
].copy()

# ============================================================
# STEP 7: CREATE RESULTS DIRECTORY
# ============================================================

import os

os.makedirs(
    "results",
    exist_ok=True
)

# ============================================================
# STEP 8: SAVE RECOMMENDATIONS
# ============================================================

recommendations.to_csv(
    output_file,
    index=False
)

# ============================================================
# STEP 9: DISPLAY RESULTS
# ============================================================

print("\n===== RECOMMENDATION SUMMARY =====")

print(
    recommendations[
        "recommended_zone"
    ].value_counts()
)

print("\n===== RELOCATION SUMMARY =====")

print(
    recommendations[
        "relocation_recommended"
    ].value_counts()
)

print("\n===== SAMPLE RECOMMENDATIONS =====")

print(
    recommendations.head(10)
)

print("\n===== OUTPUT SAVED =====")

print(output_file)

print("\n===== RECOMMENDATION GENERATION COMPLETE =====")