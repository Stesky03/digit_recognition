import json
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from pathlib import Path


def plot_interactive_analysis(work_dir_path: str):
    work_dir = Path(work_dir_path)
    json_files = list(work_dir.glob("*/stats.json"))

    data_records = []
    for j_path in json_files:
        try:
            with open(j_path, "r") as f:
                data = json.load(f)
                if "black_score" in data:
                    data_records.append({
                        "font_name": j_path.parent.name,
                        "black_score": data["black_score"]
                    })
        except (json.JSONDecodeError, OSError):
            continue

    if not data_records: return

    df = pd.DataFrame(data_records)
    df_sorted = df.sort_values(by="black_score").reset_index(drop=True)

    # Create subplots canvas
    fig = make_subplots(rows=1, cols=2, subplot_titles=("black Score Distribution", "Sorted Scores mapped to Fonts"))

    # Histogram
    fig.add_trace(
        go.Histogram(x=df["black_score"], nbinsx=100, name="Density", marker_color='#2ab0ff'),
        row=1, col=1
    )

    # Scatter plot for sorted distribution (allows hovering to see font_name)
    fig.add_trace(
        go.Scatter(
            x=df_sorted.index,
            y=df_sorted["black_score"],
            mode='markers+lines',
            text=df_sorted["font_name"],  # Hover text
            hovertemplate="Font: %{text}<br>Score: %{y:.2f}<extra></extra>",
            name="Sorted Scores",
            marker=dict(color='#ff5733', size=4)
        ),
        row=1, col=2
    )

    fig.update_layout(
        height=800,
        width=1600,
        title_text="black Score Font Analysis",
        hovermode="closest",
        template="plotly_white"
    )

    fig.update_xaxes(title_text="black Score", row=1, col=1)
    fig.update_yaxes(title_text="Count", row=1, col=1)
    fig.update_xaxes(title_text="Sorted Index", row=1, col=2)
    fig.update_yaxes(title_text="black Score", row=1, col=2)

    # Exports an interactive HTML file you can open in your browser
    fig.write_html("interactive_font_analysis.html")
    fig.show()


if __name__ == "__main__":
    plot_interactive_analysis("../../allFonts_selection")