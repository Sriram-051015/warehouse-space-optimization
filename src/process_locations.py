import pandas as pd
import os

# ============================================================
# FILE PATHS
# ============================================================

input_file = "data/raw/picks/picks.csv"
output_file = "data/processed/warehouse_locations.csv"

print("\n===== PROCESSING WAREHOUSE LOCATIONS =====")

# ============================================================
# READ PICKS IN CHUNKS
# ============================================================

chunk_size = 100000

location_results = []

for chunk_number, chunk in enumerate(
    pd.read_csv(
        input_file,
        skiprows=[1],
        chunksize=chunk_size,
        usecols=["SKU", "FROM_LOC"],
        on_bad_lines="skip"
    ),
    start=1
):

    print(f"Processing chunk {chunk_number}...")

    # Remove rows with missing values
    chunk = chunk.dropna(
        subset=["SKU", "FROM_LOC"]
    )

    # Count how many times each SKU was picked
    # from each location.
    grouped = chunk.groupby(
        ["SKU", "FROM_LOC"]
    ).size().reset_index(
        name="location_pick_count"
    )

    location_results.append(grouped)

# ============================================================
# COMBINE CHUNKS
# ============================================================

print("\n===== COMBINING LOCATION RESULTS =====")

locations = pd.concat(
    location_results,
    ignore_index=True
)

# ============================================================
# COMBINE DUPLICATE SKU + LOCATION PAIRS
# ============================================================

locations = locations.groupby(
    ["SKU", "FROM_LOC"],
    as_index=False
)["location_pick_count"].sum()

# ============================================================
# FIND MAIN LOCATION FOR EACH SKU
# ============================================================

locations = locations.sort_values(
    ["SKU", "location_pick_count"],
    ascending=[True, False]
)

main_locations = (
    locations
    .groupby("SKU")
    .first()
    .reset_index()
)

# ============================================================
# RENAME MAIN LOCATION COLUMN
# ============================================================

main_locations = main_locations.rename(
    columns={
        "FROM_LOC": "main_storage_location"
    }
)

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

main_locations.to_csv(
    output_file,
    index=False
)

# ============================================================
# DISPLAY RESULTS
# ============================================================

print("\n===== LOCATION DATASET =====")

print(
    "SKUs with locations:",
    len(main_locations)
)

print(
    "Columns:",
    main_locations.columns.tolist()
)

print("\n===== FIRST 10 ROWS =====")

print(
    main_locations.head(10)
)

print("\n===== OUTPUT SAVED =====")

print(output_file)

print("\n===== LOCATION PROCESSING COMPLETE =====")