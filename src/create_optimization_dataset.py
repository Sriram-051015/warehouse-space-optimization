import pandas as pd
import os

# ============================================================
# FILE PATHS
# ============================================================

sku_file = "data/raw/SKUs/SKUs.csv"
movement_file = "data/processed/sku_movement.csv"
output_file = "data/processed/warehouse_optimization_data.csv"

print("\n===== CREATING OPTIMIZATION DATASET =====")

# ============================================================
# STEP 1: READ SKU DATA
# ============================================================

print("\nReading SKU data...")

skus = pd.read_csv(
    sku_file,
    skiprows=[1],
    on_bad_lines="skip"
)

# ============================================================
# STEP 2: READ MOVEMENT DATA
# ============================================================

print("Reading movement data...")

movement = pd.read_csv(
    movement_file
)

# ============================================================
# STEP 3: CONVERT DIMENSION COLUMNS TO NUMERIC
# ============================================================

dimension_columns = [
    "HGT1",
    "WID1",
    "DPTH1",
    "HGT2",
    "WID2",
    "DPTH2",
    "HGT3",
    "WID3",
    "DPTH3"
]

for column in dimension_columns:
    skus[column] = pd.to_numeric(
        skus[column],
        errors="coerce"
    )

# ============================================================
# STEP 4: CALCULATE PRODUCT VOLUME
# ============================================================

# We use UOM1 dimensions as the primary product dimensions.
skus["product_volume"] = (
    skus["HGT1"] *
    skus["WID1"] *
    skus["DPTH1"]
)

# ============================================================
# STEP 5: SELECT IMPORTANT COLUMNS
# ============================================================

sku_data = skus[
    [
        "SKU",
        "UOM1",
        "UOM2",
        "UOM3",
        "HGT1",
        "WID1",
        "DPTH1",
        "product_volume"
    ]
].copy()

# ============================================================
# STEP 6: MERGE SKU DATA WITH MOVEMENT DATA
# ============================================================

print("Combining SKU dimensions and movement frequency...")

optimization_data = pd.merge(
    sku_data,
    movement,
    on="SKU",
    how="inner"
)

# ============================================================
# STEP 7: REMOVE INVALID VOLUME VALUES
# ============================================================

optimization_data = optimization_data[
    optimization_data["product_volume"] > 0
]

# ============================================================
# STEP 8: CREATE OUTPUT DIRECTORY
# ============================================================

os.makedirs(
    "data/processed",
    exist_ok=True
)

# ============================================================
# STEP 9: SAVE FINAL DATASET
# ============================================================

optimization_data.to_csv(
    output_file,
    index=False
)

# ============================================================
# STEP 10: DISPLAY RESULTS
# ============================================================

print("\n===== FINAL OPTIMIZATION DATASET =====")

print(
    "Rows:",
    optimization_data.shape[0]
)

print(
    "Columns:",
    optimization_data.shape[1]
)

print("\n===== COLUMN NAMES =====")

print(
    optimization_data.columns.tolist()
)

print("\n===== FIRST 10 ROWS =====")

print(
    optimization_data.head(10)
)

print("\n===== MISSING VALUES =====")

print(
    optimization_data.isnull().sum()
)

print("\n===== OUTPUT SAVED =====")

print(output_file)

print("\n===== DATASET CREATION COMPLETE =====")