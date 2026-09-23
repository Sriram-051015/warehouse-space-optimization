import pandas as pd

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# ============================================================
# FILE PATHS
# ============================================================

input_file = "data/processed/warehouse_optimization_data.csv"
output_file = "data/processed/warehouse_clusters.csv"

print("\n===== PRODUCT CLUSTERING =====")

# ============================================================
# STEP 1: LOAD DATA
# ============================================================

data = pd.read_csv(input_file)

print("Products loaded:", len(data))

# ============================================================
# STEP 2: SELECT FEATURES
# ============================================================

features = data[
    [
        "product_volume",
        "movement_frequency"
    ]
].copy()

print("\n===== FEATURES USED FOR CLUSTERING =====")
print(features.columns.tolist())

# ============================================================
# STEP 3: SCALE FEATURES
# ============================================================

scaler = StandardScaler()

scaled_features = scaler.fit_transform(
    features
)

# ============================================================
# STEP 4: CREATE K-MEANS MODEL
# ============================================================

kmeans = KMeans(
    n_clusters=4,
    random_state=42,
    n_init=10
)

# ============================================================
# STEP 5: TRAIN CLUSTERING MODEL
# ============================================================

clusters = kmeans.fit_predict(
    scaled_features
)

# ============================================================
# STEP 6: ADD CLUSTER LABELS
# ============================================================

data["cluster"] = clusters

# ============================================================
# STEP 7: DISPLAY CLUSTER COUNTS
# ============================================================

print("\n===== CLUSTER COUNTS =====")

print(
    data["cluster"].value_counts().sort_index()
)

# ============================================================
# STEP 8: DISPLAY CLUSTER CHARACTERISTICS
# ============================================================

print("\n===== CLUSTER CHARACTERISTICS =====")

cluster_summary = data.groupby("cluster").agg(
    product_count=("SKU", "count"),
    average_volume=("product_volume", "mean"),
    average_movement=("movement_frequency", "mean")
).reset_index()

print(cluster_summary)

# ============================================================
# STEP 9: SAVE CLUSTERED DATA
# ============================================================

data.to_csv(
    output_file,
    index=False
)

print("\n===== CLUSTERED DATA SAVED =====")
print(output_file)

print("\n===== CLUSTERING COMPLETE =====")