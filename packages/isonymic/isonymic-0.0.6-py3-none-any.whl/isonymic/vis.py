import matplotlib.pyplot as plt
import indicators

PLOT_SHOW_N_POPULAR_SURNAMES = 3


def plot_log_occurrences_vs_log_frequencies(
    people_surnames_serie,
    main_annotation: str = "Region",
    ax=None,
    save_path: str = "",
    main_annotation_fontsize: int = 18,
    subtitle_annotation: str = "n=1000",
    subtitle_annotation_fontsize: int = 8,
    xmax=None,
    ymax=None,
):
    """Plots a log-log graph of occurrences versus frequencies for surnames.

    This plot is based on the method proposed by Fox, W. R., & Lasker, G. W. (1983) in
    "The distribution of surname frequencies". International Statistical Review/Revue
    Internationale de Statistique, 81-87.

    Args:
        people_surnames_serie (pd.Series): Series containing the surnames of the population.
        main_annotation (str, optional): Name of the region where the surnames were recorded. Defaults to "Region".
        ax (matplotlib.axes.Axes, optional): Matplotlib axes object. If None, a new figure and axes are created. Defaults to None.
        save_path (str, optional): Path to save the plot. If provided, the plot is saved to this path, otherwise the axes are returned. Defaults to "".
        main_annotation_fontsize (int, optional): Font size for the main annotation text. Defaults to 18.
        subtitle_annotation (str, optional): Subtitle text for additional context (e.g., sample size). Defaults to "n=1000".
        subtitle_annotation_fontsize (int, optional): Font size for the subtitle text. Defaults to 8.
        xmax (float, optional): Maximum x-axis value for the plot. Defaults to None.
        ymax (float, optional): Maximum y-axis value for the plot. Defaults to None.

    Returns:
        matplotlib.axes.Axes: The axes of the plot, unless a save path is provided.

    Raises:
        ValueError: If the input series is empty.
    """
    if people_surnames_serie.empty:
        raise ValueError("The surnames series must not be empty.")

    s_value = len(people_surnames_serie.unique())
    n_value = len(people_surnames_serie)
    occur_vs_freq_df = indicators.get_occurrences_vs_frequencies(people_surnames_serie)
    occurrences_log = occur_vs_freq_df["occurrences_log"]
    frequency_log = occur_vs_freq_df["frecuency_log"]

    if ax is None:
        f, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 8), constrained_layout=True)

    ax.scatter(occurrences_log, frequency_log, alpha=0.25)

    ax.annotate(
        f"{main_annotation}",
        xy=(0.75, 0.75),
        xycoords="axes fraction",
        fontsize=main_annotation_fontsize,
        va="top",
        ha="left",
    )

    subtitle_annotation = f"n = {n_value:,}\ns = {s_value:,}"
    ax.annotate(
        f"{subtitle_annotation}",
        xy=(0.75, 0.69),
        xycoords="axes fraction",
        fontsize=subtitle_annotation_fontsize,
        color="grey",
        va="top",
        ha="left",
    )

    ax.spines.right.set_visible(False)
    ax.spines.top.set_visible(False)
    ax.set_xlabel("Log(Occurrences)")
    ax.set_ylabel("Log(Frequencies)")

    ax.set_xlim(-0.25, xmax)
    ax.set_ylim(-0.25, ymax)

    (
        _,
        surnames_with_minimal_frequency,
        max_frequencies,
        surnames_with_max_frequencies,
    ) = indicators.get_surname_frequencies2(people_surnames_serie)

    surnames_with_minimal_frequency_n = len(surnames_with_minimal_frequency)

    selected_columns = ["frecuency_log", "occurrences_log"]
    ycoord_for_min_freq, xcoord_for_min_occur = (
        occur_vs_freq_df.sort_values(by="occurrences_log", ascending=True)
        .reset_index(drop=True)
        .loc[0, selected_columns]
        .to_dict()
        .values()
    )

    ax.annotate(
        f"{surnames_with_minimal_frequency_n:,} surnames with a single bearer",
        xy=(xcoord_for_min_occur, ycoord_for_min_freq),
        xytext=(0.1, 0.9),
        textcoords="axes fraction",
        fontsize=10,
        color="grey",
        arrowprops=dict(arrowstyle="->", color="lightgrey"),
    )

    ycoord_for_max_freq, xcoord_for_max_occur = (
        occur_vs_freq_df.sort_values(by="occurrences_log", ascending=False)
        .reset_index(drop=True)
        .loc[0, selected_columns]
        .to_dict()
        .values()
    )

    for i, (occurrence_i, surname_i) in enumerate(
        zip(
            max_frequencies[:PLOT_SHOW_N_POPULAR_SURNAMES],
            surnames_with_max_frequencies[:PLOT_SHOW_N_POPULAR_SURNAMES],
        )
    ):
        f = occur_vs_freq_df.loc[
            occur_vs_freq_df["occurrences"] == occurrence_i, "frecuency_log"
        ]
        ycoord_for_max_freq = f[f.first_valid_index()]

        f = occur_vs_freq_df.loc[
            occur_vs_freq_df["occurrences"] == occurrence_i, "occurrences_log"
        ]
        xcoord_for_max_occur = f[f.first_valid_index()]

        ax.annotate(
            f"{surname_i} ({occurrence_i})",
            xy=(xcoord_for_max_occur, ycoord_for_max_freq),
            xytext=(0.85 - (0.1 * i), 0.25 + (0.045 * i)),
            textcoords="axes fraction",
            fontsize=6,
            color="grey",
            horizontalalignment="left",
            verticalalignment="center_baseline",
            arrowprops=dict(
                arrowstyle="->",
                color="lightgrey",
                connectionstyle="arc3,rad=-0.2",
            ),
        )

    if save_path:
        plt.savefig(save_path)
        plt.close()
    else:
        return ax
