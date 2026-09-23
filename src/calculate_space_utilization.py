import pandas as pd
import os

input_file = "results/warehouse_placement_recommendations.csv"
output_file = "results/space_utilization_summary.csv"

print("\n===== CALCULATING SPACE UTILIZATION =====")

# ============================================================
# STEP 1: LOAD RECOMMENDATIONS
# ============================================================

data = pd.read_csv(input_file)

print("Products loaded:", len(data))

# ============================================================
# STEP 2: CALCULATE TOTAL PRODUCT VOLUME
# ============================================================

total_product_volume = data[
    "product_volume"
].sum()

print("\n===== TOTAL PRODUCT SPACE =====")

print(
    "Total product volume:",
    total_product_volume
)

# ============================================================
# STEP 3: CALCULATE SPACE BY ZONE
# ============================================================

zone_summary = data.groupby(
    "recommended_zone"
).agg(
    product_count=("SKU", "count"),
    total_volume=("product_volume", "sum")
).reset_index()

# ============================================================
# STEP 4: CALCULATE PERCENTAGE OF TOTAL SPACE
# ============================================================

zone_summary["space_percentage"] = (
    zone_summary["total_volume"]
    / total_product_volume
    * 100
)

# ============================================================
# STEP 5: CALCULATE PRODUCT COUNT PERCENTAGE
# ============================================================

total_products = len(data)

zone_summary["product_percentage"] = (
    zone_summary["product_count"]
    / total_products
    * 100
)

# ============================================================
# STEP 6: DISPLAY RESULTS
# ============================================================

print("\n===== SPACE UTILIZATION BY ZONE =====")

print(
    zone_summary
)

print("\n===== TOTAL PRODUCTS =====")

print(
    total_products
)

print("\n===== TOTAL PRODUCT VOLUME =====")

print(
    total_product_volume
)

# ============================================================
# STEP 7: SAVE RESULTS
# ============================================================

os.makedirs(
    "results",
    exist_ok=True
)

zone_summary.to_csv(
    output_file,
    index=False
)

print("\n===== OUTPUT SAVED =====")

print(output_file)

print("\n===== SPACE UTILIZATION CALCULATION COMPLETE =====")