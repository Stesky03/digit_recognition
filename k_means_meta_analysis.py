import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.cluster import KMeans


def load_pca_features(fonts_path):
    """Loads the pre-computed PCA vectors from the JSON files."""
    features = []
    print("Loading PCA features from disk...")
    dirs = [d for d in fonts_path.iterdir() if d.is_dir()]

    for font_dir in sorted(dirs):
        json_path = font_dir / "stats.json"
        if json_path.exists():
            with open(json_path, "r") as f:
                data = json.load(f)
                if "PCA_GAP" in data:
                    features.append(data["PCA_GAP"])
                else:
                    print(f"Warning: No PCA_GAP in {font_dir.name}")

    return np.array(features)


def find_analytical_elbow(k_values, inertias):
    """
    Finds the elbow by calculating the maximum perpendicular distance
    from the curve to the line connecting the first and last points.
    """
    # Coordinates of the line connecting first and last point
    p1 = np.array([k_values[0], inertias[0]])
    p2 = np.array([k_values[-1], inertias[-1]])

    distances = []
    for k, inertia in zip(k_values, inertias):
        p0 = np.array([k, inertia])
        # Calculate perpendicular distance
        # Formula: |(x2-x1)(y1-y0) - (x1-x0)(y2-y1)| / |p2 - p1|
        numerator = np.abs((p2[0] - p1[0]) * (p1[1] - p0[1]) - (p1[0] - p0[0]) * (p2[1] - p1[1]))
        denominator = np.linalg.norm(p2 - p1)
        distances.append(numerator / denominator)

    # The elbow is the point with the maximum distance to the chord
    optimal_idx = np.argmax(distances)
    return k_values[optimal_idx], distances


def run_kmeans_sweep(data, k_start=2, k_end=60, step=2):
    """Executes K-means across the defined range and plots the result."""
    k_values = list(range(k_start, k_end + 1, step))
    inertias = []

    print(f"Running K-Means sweep from k={k_start} to k={k_end}...")
    for k in k_values:
        # n_init='auto' suppresses warnings and speeds up the search
        kmeans = KMeans(n_clusters=k, n_init='auto', random_state=42)
        kmeans.fit(data)
        inertias.append(kmeans.inertia_)
        print(f"k={k:02d} | Inertia: {kmeans.inertia_:.2f}")

    # Calculate the critical point mathematically
    optimal_k, distances = find_analytical_elbow(k_values, inertias)
    print(f"\nOptimal K computed analytically: {optimal_k}")

    # Visualization
    fig, ax1 = plt.subplots(figsize=(10, 6))

    ax1.plot(k_values, inertias, 'b-o', label='Inertia (WCSS)')
    ax1.set_xlabel('Number of Clusters (k)')
    ax1.set_ylabel('Inertia', color='b')
    ax1.tick_params('y', colors='b')
    ax1.grid(True, linestyle='--', alpha=0.7)

    # Plot the chord line used for distance calculation
    ax1.plot([k_values[0], k_values[-1]], [inertias[0], inertias[-1]], 'k--', alpha=0.5, label='Chord')

    # Highlight the optimal K
    ax1.axvline(x=optimal_k, color='r', linestyle='--', label=f'Optimal k = {optimal_k}')

    plt.title('K-Means Clustering: Elbow Method')
    plt.legend()
    plt.tight_layout()
    plt.savefig("kmeans_elbow.png", dpi=300)
    plt.show()

    return optimal_k


if __name__ == "__main__":
    input_path = Path("../../processed_fonts")

    # 1. Load data
    pca_matrix = load_pca_features(input_path)

    if pca_matrix.size > 0:
        print(f"Data shape: {pca_matrix.shape}")
        # 2. Run the sweep
        # Adjust k_end based on how granular your font categories need to be
        best_k = run_kmeans_sweep(pca_matrix, k_start=2, k_end=80, step=2)

        # 3. Optional: Run final fit with best_k and save labels here
    else:
        print("Error: No data loaded.")