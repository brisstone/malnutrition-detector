import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st


def render_confusion_heatmap(cm: list, classes: list[str], title: str) -> None:
    matrix = np.array(cm)
    fig, ax = plt.subplots(figsize=(4.2, 3.4))
    im = ax.imshow(matrix, cmap="YlOrBr", aspect="auto")

    ax.set_xticks(range(len(classes)))
    ax.set_yticks(range(len(classes)))
    ax.set_xticklabels(classes, rotation=30, ha="right")
    ax.set_yticklabels(classes)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_title(title, fontsize=10, fontweight="bold", pad=10)

    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            color = "white" if matrix[i, j] > matrix.max() * 0.55 else "#3d2314"
            ax.text(j, i, int(matrix[i, j]), ha="center", va="center", color=color, fontsize=9)

    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    st.pyplot(fig, clear_figure=True)


def render_confusion_matrix_table(cm: list, classes: list[str]) -> pd.DataFrame:
    df = pd.DataFrame(cm, index=classes, columns=classes)
    df.index.name = "Actual"
    df.columns.name = "Predicted"
    return df
