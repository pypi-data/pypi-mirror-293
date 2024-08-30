from typing import TYPE_CHECKING, List, Literal, Optional

import numpy as np
import requires
from scipy import spatial
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.metrics import average_precision_score, precision_recall_curve

from embdata.utils.import_utils import import_plt, smart_import

if TYPE_CHECKING:
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import plotly.express as px
    from openai import OpenAI
    client = OpenAI(max_retries=5)


def plot_array(
    array: np.ndarray,
    labels: List[str] | None = None,
    backend: Literal["matplotlib", "plotext"] = "plotext",
    xstep: float = 0.1,
    xlabel: str = "Time",
    title: str = "Trajectory",
) -> None:
    """Plot the trajectory for arbitrary action spaces, showing each dimension individually.

    Args:
      trajectory (np.ndarray): The trajectory array.
      labels (list[str], optional): The labels for each dimension of the trajectory. Defaults to None.
      backend (Literal["matplotlib", "plotext"], optional): The plotting backend to use. Defaults to "plotext".
      time_step (float, optional): The time step between each step in the trajectory. Defaults to 0.1.

    Returns:
      None
    """
    plt = import_plt(backend)
    plt.clear_figure()
    # plt.active().cld()
    # plt.clc()

    n_dims = array.shape[1]
    if labels is None or len(labels) != n_dims:
        labels = [f"Dim{i}" for i in range(n_dims)]

    xaxis = np.arange(len(array)) * xstep
    # Calculate the number of rows and columns for subplots
    n_rows = (n_dims + 1) // 2  # +1 to round up
    n_cols = 2

    plt = plt.subplots(n_rows, n_cols)
    plt.theme("fhd")
    plt.title(title)
    for i in range(n_dims):
        row = i // n_cols + 1
        col = i % n_cols + 1
        subplot = plt.subplot(row, col)
        subplot.plot(xaxis, array[:, i])
        subplot.title(f"{labels[i]}")
        subplot.xlabel(xlabel)
        subplot.ylabel(labels[i])
        y_min, y_max = np.min(array[:, i]), np.max(array[:, i])
        subplot.ylim(y_min, y_max)

    # # If there's an odd number of dimensions, add a blank subplot
    # if n_dims % 2 != 0:
    #     plt.subplot(n_rows, n_cols)
    #     plt.title("Unused subplot")

    return plt

def plot_varied(
    trajectory: np.ndarray,
    labels: List[str] | None = None,
    backend: Literal["matplotlib", "plotext"] = "plotext",
    time_step: float = 0.1,
) -> None:
    """Plot the trajectory for arbitrary action spaces.

    Args:
      trajectory (np.ndarray): The trajectory array.
      labels (list[str], optional): The labels for each dimension of the trajectory. Defaults to None.
      backend (Literal["matplotlib", "plotext"], optional): The plotting backend to use. Defaults to "plotext".
      time_step (float, optional): The time step between each step in the trajectory. Defaults to 0.1.

    Returns:
      None
    """
    plt = import_plt(backend)
    plt.clf()
    plt.subplots(1, 2)
    plt.subplot(1, 1).plotsize(plt.tw() // 2, None)
    plt.subplot(1, 1).subplots(3, 1)
    plt.subplot(1, 2).subplots(2, 1)
    plt.subplot(1, 1).ticks_style("bold")

    n_dims = trajectory.shape[1]
    if labels is None or len(labels) != n_dims:
        labels = [f"Dim{i}" for i in range(n_dims)]

    time = np.arange(len(trajectory)) * time_step

    # Left column, first plot: 3D-like plot of first three dimensions
    plt.subplot(1, 1).subplot(1, 1)
    plt.theme("fhd")
    dim_count = min(3, n_dims)
    for i in range(dim_count):
        for j in range(i + 1, dim_count):
            plt.scatter(trajectory[:, i], trajectory[:, j], label=f"{labels[i]}-{labels[j]}")
    plt.title("3D Trajectory Projections")
    plt.xlabel(labels[0])
    plt.ylabel(labels[1])

    # Left column, second plot: Next three dimensions (if available)
    plt.subplot(1, 1).subplot(2, 1)
    plt.theme("fhd")
    dim_start = 3
    dim_end = min(6, n_dims)
    if dim_end > dim_start:
        for i in range(dim_start, dim_end):
            plt.plot(time, trajectory[:, i], label=labels[i])
        plt.title("Additional Dimensions")
        plt.xlabel("Time")
        plt.ylabel("Value")
    else:
        plt.title("No additional dimensions to plot")

    # Left column, third plot: Histogram of the third dimension (if available)
    plt.subplot(1, 1).subplot(3, 1)
    plt.theme("fhd")
    if n_dims > 2:
        plt.hist(trajectory[:, 2], bins=18)
        plt.title(f"Histogram of {labels[2]}")
        plt.xlabel(labels[2])
        plt.ylabel("Frequency")
    else:
        plt.title("Histogram (Not enough dimensions)")

    # Right column, first plot: First two dimensions over time
    plt.subplot(1, 2).subplot(1, 1)
    plt.theme("fhd")
    plt.title("First Two Dimensions Over Time")
    for i in range(min(2, n_dims)):
        plt.plot(time, trajectory[:, i], label=f"{labels[i]} trajectory")
    plt.xlabel("Time")
    plt.ylabel("Value")

    # Right column, second plot: Last dimension (if available)
    plt.subplot(1, 2).subplot(2, 1)
    plt.theme("fhd")
    plt.plotsize(2 * plt.tw() // 3, plt.th() // 2)
    if n_dims > 6:
        plt.plot(time, trajectory[:, -1])
        plt.title(f"{labels[-1]} Over Time")
        plt.xlabel("Time")
        plt.ylabel(labels[-1])
    else:
        plt.title("Not enough dimensions for additional plot")

    return plt

@requires("openai")
def get_embedding(text: str, model="text-embedding-3-small", **kwargs) -> List[float]:
    openai = smart_import("openai")

    client = openai.OpenAI()
    # replace newlines, which can negatively affect performance.
    text = text.replace("\n", " ")

    response = client.embeddings.create(input=[text], model=model, **kwargs)

    return response.data[0].embedding

@requires("openai")
async def aget_embedding(
    text: str, model="text-embedding-3-small", **kwargs,
) -> List[float]:
    # replace newlines, which can negatively affect performance.
    text = text.replace("\n", " ")
    openai = smart_import("openai")
    client = openai.OpenAI()
    return (await client.embeddings.create(input=[text], model=model, **kwargs))[
        "data"
    ][0]["embedding"]

@requires("openai")
def get_embeddings(
    list_of_text: List[str], model="text-embedding-3-small", **kwargs,
) -> List[List[float]]:
    assert len(list_of_text) <= 2048, "The batch size should not be larger than 2048."

    # replace newlines, which can negatively affect performance.
    list_of_text = [text.replace("\n", " ") for text in list_of_text]

    data = client.embeddings.create(input=list_of_text, model=model, **kwargs).data
    return [d.embedding for d in data]

@requires("openai")
async def aget_embeddings(
    list_of_text: List[str], model="text-embedding-3-small", **kwargs,
) -> List[List[float]]:
    assert len(list_of_text) <= 2048, "The batch size should not be larger than 2048."

    # replace newlines, which can negatively affect performance.
    list_of_text = [text.replace("\n", " ") for text in list_of_text]
    openai = smart_import("openai")
    client = openai.OpenAI()
    data = (
        await client.embeddings.create(input=list_of_text, model=model, **kwargs)
    ).data
    return [d.embedding for d in data]


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

@requires("pandas")
def plot_multiclass_precision_recall(
    y_score, y_true_untransformed, class_list, classifier_name,
):
    """Precision-Recall plotting for a multiclass problem. It plots average precision-recall, per class precision recall and reference f1 contours.

    Code slightly modified, but heavily based on https://scikit-learn.org/stable/auto_examples/model_selection/plot_precision_recall.html
    """
    pd = smart_import("pandas")
    n_classes = len(class_list)
    y_true = pd.concat(
        [(y_true_untransformed == class_list[i]) for i in range(n_classes)], axis=1,
    ).to_numpy()

    # For each class
    precision = dict()
    recall = dict()
    average_precision = dict()
    for i in range(n_classes):
        precision[i], recall[i], _ = precision_recall_curve(y_true[:, i], y_score[:, i])
        average_precision[i] = average_precision_score(y_true[:, i], y_score[:, i])

    # A "micro-average": quantifying score on all classes jointly
    precision_micro, recall_micro, _ = precision_recall_curve(
        y_true.ravel(), y_score.ravel()
    )
    average_precision_micro = average_precision_score(y_true, y_score, average="micro")
    plt.title(
        str(classifier_name)
        + f" - Average precision score over all classes: {average_precision_micro:0.2f}",
    )

    # setup plot details
    plt.figure(figsize=(9, 10))
    f_scores = np.linspace(0.2, 0.8, num=4)
    lines = []
    labels = []
    for f_score in f_scores:
        x = np.linspace(0.01, 1)
        y = f_score * x / (2 * x - f_score)
        (l,) = plt.plot(x[y >= 0], y[y >= 0], color="gray", alpha=0.2)
        plt.annotate(f"f1={f_score:0.1f}", xy=(0.9, y[45] + 0.02))

    lines.append(l)
    labels.append("iso-f1 curves")
    (l,) = plt.plot(recall_micro, precision_micro, color="gold", lw=2)
    lines.append(l)
    labels.append(
        f"average Precision-recall (auprc = {average_precision_micro:0.2f})",
    )

    for i in range(n_classes):
        (l,) = plt.plot(recall[i], precision[i], lw=2)
        lines.append(l)
        labels.append(
            f"Precision-recall for class `{class_list[i]}` (auprc = {average_precision[i]:0.2f})"
            "",
        )

    fig = plt.gcf()
    fig.subplots_adjust(bottom=0.25)
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.title(f"{classifier_name}: Precision-Recall curve for each class")
    plt.legend(lines, labels)


def distances_from_embeddings(
    query_embedding: List[float],
    embeddings: List[List[float]],
    distance_metric="cosine",
) -> List[List]:
    """Return the distances between a query embedding and a list of embeddings."""
    distance_metrics = {
        "cosine": spatial.distance.cosine,
        "L1": spatial.distance.cityblock,
        "L2": spatial.distance.euclidean,
        "Linf": spatial.distance.chebyshev,
    }
    return [
        distance_metrics[distance_metric](query_embedding, embedding)
        for embedding in embeddings
    ]


def indices_of_nearest_neighbors_from_distances(distances) -> np.ndarray:
    """Return a list of indices of nearest neighbors from a list of distances."""
    return np.argsort(distances)


def pca_components_from_embeddings(
    embeddings: List[List[float]], n_components=2,
) -> np.ndarray:
    """Return the PCA components of a list of embeddings."""
    pca = PCA(n_components=n_components)
    array_of_embeddings = np.array(embeddings)
    return pca.fit_transform(array_of_embeddings)


def tsne_components_from_embeddings(
    embeddings: List[List[float]], n_components=2, **kwargs,
) -> np.ndarray:
    """Returns t-SNE components of a list of embeddings."""
    tsne = smart_import("TSNE")
    # use better defaults if not specified
    if "init" not in kwargs:
        kwargs["init"] = "pca"
    if "learning_rate" not in kwargs:
        kwargs["learning_rate"] = "auto"
    tsne = TSNE(n_components=n_components, **kwargs)
    array_of_embeddings = np.array(embeddings)
    return tsne.fit_transform(array_of_embeddings)

@requires("pandas")
@requires("plotly")
def chart_from_components(
    components: np.ndarray,
    labels: Optional[List[str]] = None,
    strings: Optional[List[str]] = None,
    x_title="Component 0",
    y_title="Component 1",
    mark_size=5,
    **kwargs,
):
    """Return an interactive 2D chart of embedding components."""
    empty_list = ["" for _ in components]
    pd = smart_import("pandas")
    px = smart_import("plotly.express")
    data = pd.DataFrame(
        {
            x_title: components[:, 0],
            y_title: components[:, 1],
            "label": labels if labels else empty_list,
            "string": ["<br>".join(tr.wrap(string, width=30)) for string in strings]
            if strings
            else empty_list,
        },
    )
    return px.scatter(
        data,
        x=x_title,
        y=y_title,
        color="label" if labels else None,
        symbol="label" if labels else None,
        hover_data=["string"] if strings else None,
        **kwargs,
    ).update_traces(marker={"size": mark_size})


@requires("pandas")
@requires("plotly")
def chart_from_components_3D(
    components: np.ndarray,
    labels: List[str] | None = None,
    strings: List[str] | None = None,
    x_title: str = "Component 0",
    y_title: str = "Component 1",
    z_title: str = "Compontent 2",
    mark_size: int = 5,
    **kwargs,
):
    """Return an interactive 3D chart of embedding components."""
    pd = smart_import("pandas")
    px = smart_import("plotly.express")
    tr = smart_import("textwrap")
    empty_list = ["" for _ in components]
    data = pd.DataFrame(
        {
            x_title: components[:, 0],
            y_title: components[:, 1],
            z_title: components[:, 2],
            "label": labels if labels else empty_list,
            "string": ["<br>".join(tr.wrap(string, width=30)) for string in strings]
            if strings
            else empty_list,
        },
    )
    return px.scatter_3d(
        data,
        x=x_title,
        y=y_title,
        z=z_title,
        color="label" if labels else None,
        symbol="label" if labels else None,
        hover_data=["string"] if strings else None,
        **kwargs,
    ).update_traces(marker={"size": mark_size})
