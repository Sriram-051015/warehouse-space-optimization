import pandas as pd
import os

# ============================================================
# FILE PATHS
# ============================================================

input_file = "data/raw/picks/picks.csv"
output_file = "data/processed/sku_movement.csv"

# ============================================================
# READ PICKS DATA IN CHUNKS
# ============================================================

print("\n===== PROCESSING PICK HISTORY =====")

# The picks file is large, so we process it in smaller chunks.
chunk_size = 100000

results = []

for chunk_number, chunk in enumerate(
    pd.read_csv(
        input_file,
        skiprows=[1],
        chunksize=chunk_size,
        on_bad_lines="skip"
    ),
    start=1
):

    print(f"Processing chunk {chunk_number}...")

    # Convert quantity columns to numeric
    chunk["ACT_QTY"] = pd.to_numeric(
        chunk["ACT_QTY"],
        errors="coerce"
    )

    # Remove rows where SKU or quantity is invalid
    chunk = chunk.dropna(
        subset=["SKU", "ACT_QTY"]
    )

    # --------------------------------------------------------
    # Calculate movement information for this chunk
    # --------------------------------------------------------

    grouped = chunk.groupby("SKU").agg(
        pick_count=("SKU", "count"),
        total_quantity_picked=("ACT_QTY", "sum")
    ).reset_index()

    results.append(grouped)

# ============================================================
# COMBINE ALL CHUNKS
# ============================================================

print("\n===== COMBINING RESULTS =====")

movement = pd.concat(
    results,
    ignore_index=True
)

# ============================================================
# FINAL GROUPING
# ============================================================

movement = movement.groupby("SKU").agg(
    pick_count=("pick_count", "sum"),
    total_quantity_picked=("total_quantity_picked", "sum")
).reset_index()

# ============================================================
# CALCULATE MOVEMENT FREQUENCY
# ============================================================

movement["movement_frequency"] = movement["pick_count"]

# ============================================================
# CREATE OUTPUT DIRECTORY
# ============================================================

os.makedirs(
    "data/processed",
    exist_ok=True
)

# ============================================================
# SAVE DATASET
# ============================================================

movement.to_csv(
    output_file,
    index=False
)

# ============================================================
# DISPLAY RESULTS
# ============================================================

print("\n===== MOVEMENT DATASET =====")
print("Rows:", len(movement))
print("Columns:", len(movement.columns))

print("\n===== FIRST 10 ROWS =====")
print(movement.head(10))

print("\n===== SUMMARY =====")
print(movement.describe())

print("\n===== OUTPUT SAVED =====")
print(output_file)

print("\n===== PROCESSING COMPLETE =====")