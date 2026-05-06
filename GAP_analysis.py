import json
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path


def process_precomputed_deciles(base_dir_path: str):
    base_dir = Path(base_dir_path)
    print(f"[*] Checking base directory: {base_dir.absolute()}")

    if not base_dir.exists():
        print(f"[!] Error: Directory '{base_dir_path}' does not exist.")
        return

    # Identify decile directories
    decile_dirs = sorted(list(base_dir.glob("decile_*")))
    print(f"[*] Found {len(decile_dirs)} decile directories: {[d.name for d in decile_dirs]}")

    for decile_dir in decile_dirs:
        print(f"\n--- Processing {decile_dir.name} ---")

        data_records = []
        # Find all subdirectories containing stats.json
        stat_files = list(decile_dir.glob("*/stats.json"))
        print(f"[*] Found {len(stat_files)} potential stats.json files.")

        for stat_path in stat_files:
            try:
                with open(stat_path, "r") as f:
                    data = json.load(f)

                # Extract pre-calculated similarity
                if "similarity" in data:
                    similarity_val = data["similarity"]

                    # Ensure it's a numeric type for plotting
                    if isinstance(similarity_val, (int, float)):
                        data_records.append({
                            "folder_name": stat_path.parent.name,
                            "similarity": float(similarity_val)
                        })
                    else:
                        print(f"[!] Non-numeric similarity in {stat_path}: {similarity_val}")
                else:
                    # Debug: Print keys if "similarity" is missing
                    print(f"[!] Key 'similarity' missing in {stat_path}. Keys found: {list(data.keys())}")

            except Exception as e:
                print(f"[!] Error reading {stat_path}: {e}")
                continue

        if not data_records:
            print(f"[!] No valid records found for {decile_dir.name}. Skipping plot.")
            continue

        print(f"[+] Successfully gathered {len(data_records)} similarity scores.")

        # Prepare DataFrames
        df = pd.DataFrame(data_records)
        df_sorted = df.sort_values(by="similarity").reset_index(drop=True)

        # Plotting logic
        try:
            fig = make_subplots(
                rows=1, cols=2,
                subplot_titles=("Similarity Distribution", "Ranked Similarity")
            )

            # Histogram
            fig.add_trace(
                go.Histogram(
                    x=df["similarity"],
                    nbinsx=50,
                    name="Density",
                    marker_color='#2ab0ff'
                ),
                row=1, col=1
            )

            # Sorted Scatter
            fig.add_trace(
                go.Scatter(
                    x=df_sorted.index,
                    y=df_sorted["similarity"],
                    mode='markers+lines',
                    text=df_sorted["folder_name"],
                    hovertemplate="Folder: %{text}<br>Similarity: %{y:.4f}<extra></extra>",
                    name="Sorted Folders",
                    marker=dict(color='#ff5733', size=4)
                ),
                row=1, col=2
            )

            fig.update_layout(
                height=600,
                width=1400,
                title_text=f"Decile Similarity Analysis: {decile_dir.name}",
                template="plotly_white",
                showlegend=False
            )

            fig.update_xaxes(title_text="Similarity Score", row=1, col=1)
            fig.update_yaxes(title_text="Count", row=1, col=1)
            fig.update_xaxes(title_text="Sorted Rank", row=1, col=2)
            fig.update_yaxes(title_text="Similarity Score", row=1, col=2)

            output_name = f"analysis_{decile_dir.name}.html"
            fig.write_html(output_name)
            print(f"[✔] Exported: {output_name}")

        except Exception as e:
            print(f"[!] Plotly rendering failed for {decile_dir.name}: {e}")


if __name__ == "__main__":
    process_precomputed_deciles("../../processed_fonts_deciles")