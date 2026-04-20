import dash
from dash import dcc, html, Input, Output, State
import pandas as pd
import plotly.express as px
import numpy as np

# =========================
# ダミーデータ作成
# =========================
np.random.seed(42)

good = pd.DataFrame({
    "compound": [f"G{i}" for i in range(20)],
    "ΔG": np.random.uniform(-9, -7, 20),
    "std": np.random.uniform(0.1, 0.5, 20),
    "distance": np.random.uniform(1, 5, 20)
})

mid = pd.DataFrame({
    "compound": [f"M{i}" for i in range(40)],
    "ΔG": np.random.uniform(-7, -6, 40),
    "std": np.random.uniform(0.5, 1.5, 40),
    "distance": np.random.uniform(5, 10, 40)
})

bad = pd.DataFrame({
    "compound": [f"B{i}" for i in range(40)],
    "ΔG": np.random.uniform(-6, -4, 40),
    "std": np.random.uniform(1.5, 3, 40),
    "distance": np.random.uniform(10, 20, 40)
})

df = pd.concat([good, mid, bad], ignore_index=True)

# =========================
# アプリ作成
# =========================
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("分子スクリーニングダッシュボード"),

    html.Label("ΔG 閾値（低いほど厳しい）"),
    dcc.Slider(id="dg", min=-10, max=-4, step=0.1, value=-6),

    html.Label("ばらつき 上限"),
    dcc.Slider(id="std", min=0, max=3, step=0.1, value=1.5),

    html.Label("距離 上限"),
    dcc.Slider(id="dist", min=0, max=20, step=1, value=10),

    html.Br(),

    html.Button("リセット", id="reset", n_clicks=0),

    html.H3(id="count"),

    dcc.Graph(id="graph")
])

# =========================
# コールバック
# =========================
@app.callback(
    Output("graph", "figure"),
    Output("count", "children"),
    Input("dg", "value"),
    Input("std", "value"),
    Input("dist", "value")
)
def update_graph(dg, std, dist):
    filtered = df[
        (df["ΔG"] < dg) &
        (df["std"] < std) &
        (df["distance"] < dist)
    ]

    fig = px.scatter(
        filtered,
        x="distance",
        y="ΔG",
        color="std",
        hover_data=["compound"]
    )

    return fig, f"残り候補数: {len(filtered)}"

# =========================
# リセット処理
# =========================
@app.callback(
    Output("dg", "value"),
    Output("std", "value"),
    Output("dist", "value"),
    Input("reset", "n_clicks"),
    prevent_initial_call=True
)
def reset_values(n):
    return -6, 1.5, 10

# =========================
# 実行
# =========================
if __name__ == "__main__":
    app.run(debug=True)