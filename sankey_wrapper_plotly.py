import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go


def add_link(source, target, value, label=""):
    new_link = {}
    new_link["source"] = source
    new_link["target"] = target
    new_link["value"] = value,
    new_link["label"] = label,
    return new_link


def get_nodes(df_links, colormap="Paired"):
    nodes = pd.concat([df_links["source"], df_links["target"]]).unique()

    cmap = plt.get_cmap(colormap)
    colors = cmap(np.linspace(0, 1, len(nodes)))

    df_nodes = pd.DataFrame()
    df_nodes["label"] = nodes
    df_nodes["color"] = list(colors)
    df_nodes["index"] = df_nodes.index
    return df_nodes


def plot_sankey(df_links):
    df_nodes = get_nodes(df_links)

    enc_label = dict(zip(df_nodes["label"], df_nodes["index"]))
    df_links = df_links.replace(enc_label)

    dec_color = dict(zip(df_nodes["index"], df_nodes["color"]))
    dec_color = dict((k, to_rgba_str(v, 0.5)) for k, v in dec_color.items())
    df_links["color"] = df_links["source"].copy()
    df_links["color"] = df_links["color"].replace(dec_color)

    df_nodes["color"] = df_nodes["color"].apply(to_rgba_str)

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=25,
            thickness=25,
            line=dict(color="black", width=0.5),
            label=df_nodes["label"],
            color=df_nodes["color"]
        ),
        link=dict(
            source=df_links["source"],
            target=df_links["target"],
            value=df_links["value"],
            label=df_links["label"],
            color=df_links["color"]
        ))])

    fig.update_layout(title_text="Example", font_size=10)
    fig.write_html('sankey.html', auto_open=True)


def to_rgba_str(rgb_arr, alpha=None):
    if alpha is None:
        alpha = rgb_arr[-1]
    return f"rgba({rgb_arr[0]}, {rgb_arr[1]}, {rgb_arr[2]}, {alpha})"
