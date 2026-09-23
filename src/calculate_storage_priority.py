import pandas as pd

# ============================================================
# FILE PATHS
# ============================================================

input_file = "data/processed/warehouse_clusters.csv"
output_file = "data/processed/warehouse_priority.csv"

print("\n===== CALCULATING STORAGE PRIORITY =====")

# ============================================================
# STEP 1: LOAD DATA
# ============================================================

data = pd.read_csv(input_file)

print("Products loaded:", len(data))

# ============================================================
# STEP 2: CREATE PERCENTILE-BASED SCORES
# ============================================================

data["movement_score"] = (
    data["movement_frequency"]
    .rank(pct=True)
)

data["space_requirement_score"] = (
    data["product_volume"]
    .rank(pct=True)
)

# ============================================================
# STEP 3: CALCULATE STORAGE PRIORITY
# ============================================================

data["storage_priority_score"] = (
    0.70 * data["movement_score"]
    +
    0.30 * data["space_requirement_score"]
)

# ============================================================
# STEP 4: CREATE PRIORITY CATEGORY
# ============================================================

def classify_priority(score):

    if score >= 0.80:
        return "High Priority"

    elif score >= 0.40:
        return "Medium Priority"

    else:
        return "Low Priority"


data["storage_priority"] = data[
    "storage_priority_score"
].apply(classify_priority)

# ============================================================
# STEP 5: DISPLAY PRIORITY COUNTS
# ============================================================

print("\n===== PRIORITY COUNTS =====")

print(
    data["storage_priority"].value_counts()
)

# ============================================================
# STEP 6: DISPLAY TOP PRODUCTS
# ============================================================

print("\n===== TOP 10 PRIORITY PRODUCTS =====")

top_products = data.sort_values(
    "storage_priority_score",
    ascending=False
).head(10)

print(
    top_products[
        [
            "SKU",
            "product_volume",
            "movement_frequency",
            "movement_score",
            "space_requirement_score",
            "storage_priority_score",
            "storage_priority"
        ]
    ]
)

# ============================================================
# STEP 7: SAVE RESULT
# ============================================================

data.to_csv(
    output_file,
    index=False
)

print("\n===== OUTPUT SAVED =====")
print(output_file)

print("\n===== STORAGE PRIORITY COMPLETE =====")