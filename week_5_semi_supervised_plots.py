import numpy as np
from numpy.typing import ArrayLike
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.utils import Bunch
from sklearn.metrics import ConfusionMatrixDisplay
from IPython.display import display


def plot_iris(
    iris: Bunch,
    labels: ArrayLike | None = None,
    title: str = "Iris Dataset",
    palette_style: str = "deep",
    small_slice_threshold: float = 0.05,
) -> None:
    """Plot label proportions and petal measurements for the Iris dataset.

    Args:
        iris: Dataset returned by sklearn.datasets.load_iris().
        labels: One label per sample. Use species codes 0, 1, 2,
            or -1 for unlabelled samples. Defaults to iris.target.
        title: Overall title for the figure.
        palette_style: Colour palette for the plot. Use "deep" for vibrant colours
            and "pastel" for muted colours.
        small_slice_threshold: Proportion below which pie slices receive arrows.
            Defaults to 0.05 (5%).

    Unlabelled samples are shown in grey. Species colours remain
    consistent across calls.
    """
    labels = np.asarray(iris.target if labels is None else labels)

    if labels.shape != (len(iris.data),):
        raise ValueError("Provide exactly one label per flower.")

    valid_labels = [-1, *range(len(iris.target_names))]
    if not np.isin(labels, valid_labels).all():
        raise ValueError(f"Labels must be one of {valid_labels}.")

    label_names = {
        i: str(name) for i, name in enumerate(iris.target_names)
    }
    label_names[-1] = "Unlabelled"

    iris_df = pd.DataFrame(iris.data, columns=iris.feature_names)
    iris_df["Label"] = [label_names[int(label)] for label in labels]

    # Keep species colours consistent, even when some labels are absent.
    palette: dict[str, str] = dict(zip(
        map(str, iris.target_names),
        sns.color_palette(
            palette_style,
            n_colors=len(iris.target_names),
        ).as_hex(),
    ))
    palette["Unlabelled"] = "#b0b0b0"

    order = [
        name for name in palette
        if name in iris_df["Label"].values
    ]
    counts = iris_df["Label"].value_counts().reindex(order)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle(title)

    '''axes[0].pie(
        counts,
        labels=counts.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=[palette[name] for name in counts.index],
    )
    axes[0].set_title("Label Proportions")'''
    proportions = counts / counts.sum()
    small_slices = proportions < small_slice_threshold

    wedges, _ = axes[0].pie(
        counts,
        labels=[
            "" if small else name
            for name, small in zip(counts.index, small_slices)
        ],
        startangle=90,
        colors=[palette[name] for name in counts.index],
        labeldistance=1.1,
    )

    sides = {-1: [], 1: []}

    for wedge, name, proportion, small in zip(
        wedges, counts.index, proportions, small_slices
    ):
        angle = np.deg2rad((wedge.theta1 + wedge.theta2) / 2)
        x, y = np.cos(angle), np.sin(angle)

        if small:
            side = 1 if x >= 0 else -1
            sides[side].append((y, x, name, proportion))
        else:
            # Larger slices keep their percentage inside the pie.
            axes[0].text(
                0.65 * x,
                0.65 * y,
                f"{proportion:.1%}",
                ha="center",
                va="center",
            )

    # Only small slices receive external labels and arrows.
    for side, entries in sides.items():
        entries.sort(key=lambda entry: entry[0])

        if not entries:
            continue

        positions = (
            np.linspace(-1.2, 1.2, len(entries))
            if len(entries) > 1
            else [entries[0][0] * 1.2]
        )

        for (y, x, name, proportion), label_y in zip(entries, positions):
            axes[0].annotate(
                f"{name}: {proportion:.1%}",
                xy=(x, y),
                xytext=(side * 1.7, label_y),
                ha="left" if side == 1 else "right",
                va="center",
                fontsize=9,
                arrowprops={
                    "arrowstyle": "->",
                    "color": palette[name],
                    "connectionstyle": "arc3",
                },
            )

    axes[0].set_xlim(-2.6, 2.6)
    axes[0].set_ylim(-1.5, 1.5)
    axes[0].set_title("Label Proportions")

    sns.scatterplot(
        data=iris_df,
        x="petal length (cm)",
        y="petal width (cm)",
        hue="Label",
        style="Label",
        hue_order=order,
        style_order=order,
        palette=palette,
        s=65,
        ax=axes[1],
    )
    axes[1].set_title("Petal Measurements by Label")
    axes[1].set_xlabel("Petal Length (cm)")
    axes[1].set_ylabel("Petal Width (cm)")

    plt.tight_layout()
    plt.show()

def _hidden_predictions(
    predictions: ArrayLike,
    hidden: np.ndarray,
    algorithm_name: str,
) -> np.ndarray:
    """Select hidden-sample predictions, accepting full or already filtered input."""
    predictions = np.asarray(predictions)
    if predictions.shape == hidden.shape:
        return predictions[hidden]
    if predictions.shape == (int(hidden.sum()),):
        return predictions
    raise ValueError(
        f"{algorithm_name}: provide one prediction per sample ({hidden.size}) "
        f"or per hidden sample ({hidden.sum()}), in original dataset order."
    )


def plot_prediction_results(
    iris: Bunch,
    hidden: ArrayLike,
    algorithm_one_predictions: ArrayLike,
    algorithm_two_predictions: ArrayLike,
    algorithm_one_name: str,
    algorithm_two_name: str,
) -> None:
    """Compare classification results on flowers with hidden labels.

    Args:
        iris: Dataset returned by sklearn.datasets.load_iris().
        hidden: Boolean mask identifying flowers with hidden labels.
        algorithm_one_predictions: Predictions for all samples or just the
            hidden samples, in original dataset order.
        algorithm_two_predictions: Predictions for all samples or just the
            hidden samples, in original dataset order.
        algorithm_one_name: Display name for the first algorithm.
        algorithm_two_name: Display name for the second algorithm.

    Colours indicate true species. Circles indicate correct predictions;
    crosses indicate incorrect predictions.
    """
    hidden = np.asarray(hidden, dtype=bool)

    if hidden.shape != iris.target.shape:
        raise ValueError("hidden must have one entry per flower.")
    if not hidden.any():
        raise ValueError("At least one flower must have a hidden label.")
    one_predictions = _hidden_predictions(algorithm_one_predictions, hidden, algorithm_one_name)
    two_predictions = _hidden_predictions(algorithm_two_predictions, hidden, algorithm_two_name)

    true_labels = iris.target[hidden]
    plot_data = pd.DataFrame(
        iris.data[hidden],
        columns=iris.feature_names,
    )
    plot_data["True species"] = iris.target_names[true_labels]

    palette = dict(zip(
        iris.target_names,
        sns.color_palette("deep", n_colors=len(iris.target_names)),
    ))

    fig, axes = plt.subplots(
        1, 2, figsize=(15, 5), sharex=True, sharey=True
    )
    fig.suptitle(
        f"Predictions on Hidden Labels — {hidden.mean():.1%} Hidden"
    )

    for ax, predictions, title in [
        (axes[0], one_predictions, algorithm_one_name),
        (axes[1], two_predictions, algorithm_two_name),
    ]:
        correct = predictions == true_labels
        panel = plot_data.assign(
            Result=np.where(correct, "Correct", "Incorrect")
        )

        # Draw incorrect predictions last so they remain visible.
        panel = panel.sort_values("Result")

        sns.scatterplot(
            data=panel,
            x="petal length (cm)",
            y="petal width (cm)",
            hue="True species",
            hue_order=list(iris.target_names),
            palette=palette,
            style="Result",
            style_order=["Correct", "Incorrect"],
            markers={"Correct": "o", "Incorrect": "X"},
            s=85,
            ax=ax,
        )

        ax.set_title(
            f"{title}\n"
            f"{correct.sum()}/{len(correct)} correct ({correct.mean():.1%})"
        )
        ax.set_xlabel("Petal Length (cm)")
        ax.set_ylabel("Petal Width (cm)")

    plt.tight_layout()
    plt.show()

def plot_confusion_matrices(
    true_labels: ArrayLike,
    hidden: ArrayLike,
    algorithm_one_predictions: ArrayLike,
    algorithm_two_predictions: ArrayLike,
    class_names: ArrayLike,
    algorithm_one_name: str,
    algorithm_two_name: str,
) -> None:
    """Compare both models on samples whose labels were hidden.

    Args:
        true_labels: True labels for the complete dataset.
        hidden: Boolean mask identifying samples with hidden labels.
        algorithm_one_predictions: Predictions for all samples or just the
            hidden samples, in original dataset order.
        algorithm_two_predictions: Predictions for all samples or just the
            hidden samples, in original dataset order.
        algorithm_one_name: Display name for the first algorithm.
        algorithm_two_name: Display name for the second algorithm.
        class_names: Names corresponding to class codes 0, 1, 2, etc.

    Displays counts for each true/predicted class combination.
    The title reports the actual proportion of hidden labels.
    """
    true_labels = np.asarray(true_labels)
    hidden = np.asarray(hidden, dtype=bool)

    class_names = np.asarray(class_names)

    if class_names.ndim != 1:
        raise ValueError("class_names must be a one-dimensional array of names.")

    if hidden.shape != true_labels.shape:
        raise ValueError("hidden must have one entry per true label.")
    if not hidden.any():
        raise ValueError("At least one sample must have a hidden label.")

    one_predictions = _hidden_predictions(algorithm_one_predictions, hidden, algorithm_one_name)
    two_predictions = _hidden_predictions(algorithm_two_predictions, hidden, algorithm_two_name)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle(
        f"Hidden Labels: {hidden.mean():.1%} "
        f"({hidden.sum()} of {hidden.size} samples)"
    )

    for ax, predictions, title in [
        (axes[0], one_predictions, algorithm_one_name),
        (axes[1], two_predictions, algorithm_two_name),
    ]:
        ConfusionMatrixDisplay.from_predictions(
            true_labels[hidden],
            predictions,
            labels=range(len(class_names)),
            display_labels=class_names,
            cmap="Blues",
            colorbar=False,
            values_format="d",
            ax=ax,
        )
        ax.set_title(title)

    plt.tight_layout()
    plt.show()


def display_coloured_labels(
    labels: ArrayLike,
    n_classes: int = 3,
    palette_style: str = "deep",
    max_per_row: int | None = None,
) -> None:
    r"""Display class labels in colour for notebooks and PDF exports.

    Args:
        labels: One-dimensional array of class codes, with -1 for unlabelled.
        n_classes: Number of classes, numbered from 0 to n_classes - 1.
        palette_style: Seaborn colour palette for the classes.
        max_per_row: Maximum number of labels per row. None uses automatic
            wrapping. Narrow displays or pages may wrap rows earlier.

    Unlabelled samples appear in grey. PDF export requires xcolor.
    """
    labels = np.asarray(labels)

    if labels.ndim != 1:
        raise ValueError("labels must be a one-dimensional array.")
    if n_classes < 1:
        raise ValueError("n_classes must be at least 1.")
    if max_per_row is not None:
        if isinstance(max_per_row, bool) or not isinstance(max_per_row, int):
            raise TypeError("max_per_row must be an integer or None.")
        if max_per_row < 1:
            raise ValueError("max_per_row must be at least 1.")
    if not np.isin(labels, [-1, *range(n_classes)]).all():
        raise ValueError(
            f"Labels must be -1 or class codes from 0 to {n_classes - 1}."
        )

    colours: dict[int, str] = dict(enumerate(
        sns.color_palette(palette_style, n_colors=n_classes).as_hex()
    ))
    colours[-1] = "#808080"

    row_size = max_per_row or max(len(labels), 1)
    rows = [
        labels[start:start + row_size]
        for start in range(0, len(labels), row_size)
    ]

    html_rows = []
    latex_rows = []
    plain_rows = []

    for row in rows:
        html_rows.append(" ".join(
            f'<span style="color: {colours[int(label)]}; '
            f'font-weight: bold;">{int(label):2d}</span>'
            for label in row
        ))

        latex_rows.append(" ".join(
            r"\textcolor[HTML]{"
            + colours[int(label)].lstrip("#").upper()
            + r"}{\texttt{"
            + str(int(label))
            + "}}"
            for label in row
        ))

        plain_rows.append(" ".join(f"{int(label):2d}" for label in row))

    html_content = "[" + "\n".join(html_rows) + "]"
    latex_content = "[" + "\n\\par\n".join(latex_rows) + "]"
    plain_content = "[" + "\n".join(plain_rows) + "]"

    display(
        {
            "text/html": (
                '<pre style="white-space: pre-wrap;">'
                + html_content
                + "</pre>"
            ),
            "text/latex": (
                r"\begin{quote}\raggedright"
                r"\setlength{\parindent}{0pt}"
                r"\setlength{\parskip}{0pt}"
                "\n" + latex_content + "\n"
                r"\end{quote}"
            ),
            "text/plain": plain_content,
        },
        raw=True,
    )